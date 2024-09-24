import os, re, json, gspread
import pandas as pd


def retrieve_df_list_from_csv(folder_fullpath=os.path.join(os.getcwd(), 'input')):
    file_list = []
    for i, f in enumerate(os.listdir(folder_fullpath)):
        if '.csv' in f.lower():
            df = pd.read_csv(os.path.join(os.getcwd(), 'input', f))
            file_list.append(df)
            print(f"File {i+1}: {f} loaded with {df.count()} records")
    return file_list


def get_completion_from_messages(client, messages, model="gpt-4o", temperature=0, max_tokens=500):
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
    )
    return response.choices[0].message.content


def extract_json_from_response(response: str):
    # Define the regular expression pattern to match JSON in the response
    json_pattern = r'\{.*\}'

    # Search for the JSON in the response
    match = re.search(json_pattern, response, re.DOTALL)

    if match:
        json_str = match.group(0)
        return json_str
    else:
        print("Error: No JSON found in the model response.")
        return None


def parse_raw_csv(gpt_client, file_list, model="gpt-4o"):
    from configs.config_gpt import delimiter, system_message_parsing
    res = []
    for in_file in file_list:
        for row in in_file.to_dict('records'):
            messages = [
            {'role': 'system',
             'content': system_message_parsing},
            {'role': 'user',
             'content': f"{delimiter}{row}{delimiter}"},
            ]
            response = get_completion_from_messages(gpt_client, messages, model)
            parsed_json = extract_json_from_response(response)
            res.append(json.loads(parsed_json))

    aggregate_book = pd.DataFrame.from_records(res).sort_values("Date").reset_index(drop=True)
    return aggregate_book


def assign_category_and_subcategory(gpt_client, aggregate_book, model="gpt-4o"):
    from dataframe_configs import categories, get_subcategories
    from configs.config_gpt import delimiter, system_message_category

    cate_res = []

    cate_str = "\n".join(f"Category: {c.name}\nDescription: {c.description}\nExample:{c.example}\n" for c in categories)

    for row in aggregate_book.to_dict('records'):
        messages = [
            {'role': 'system',
             'content': system_message_category.format(delimiter=delimiter, cate_str=cate_str)},
            {'role': 'user',
             'content': f"{delimiter}{row}{delimiter}"},
        ]

        response = get_completion_from_messages(gpt_client, messages, model)
        parsed_json = extract_json_from_response(response)
        response_str = str(json.loads(parsed_json)['Category'])
        row["Category"] = response_str

        if response_str in [c.name for c in categories]:
            cur_subcates = get_subcategories(response_str, categories)
            subcate_str = "\n".join(
                f"Subcategory: {c.name}\nDescription: {c.description}\nExample:{c.example}\n" for c in cur_subcates)
            messages = [
                {'role': 'system',
                 'content': system_message_category.format(delimiter=delimiter, cate_str=subcate_str)},
                {'role': 'user',
                 'content': f"{delimiter}{row}{delimiter}"},
            ]
            response = get_completion_from_messages(gpt_client, messages, model)
            parsed_json = extract_json_from_response(response)
            row["Subcategory"] = json.loads(parsed_json)['Category']
            cate_res.append(row)
            # print(row)
        else:
            print("Error: The response provided by the model is not a valid category defined.")
    return cate_res


def update_log_sheet(log_sheet: gspread.worksheet, audit_df: pd.DataFrame, threshold: int = 5):
    from datetime import datetime
    list_of_dicts = log_sheet.get_all_records()

    audit_df['LogDate'] = str(datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'))

    if not list_of_dicts:
        log_sheet.update([audit_df.columns.to_list()], "A1")
        log_sheet.update(audit_df.values.tolist(), "A2")
    else:
        old_logs = pd.DataFrame(list_of_dicts)
        new_logs = pd.concat([old_logs, audit_df])
        new_logs = new_logs.sort_values(['LogDate', 'Date']).reset_index(drop=True)
        new_logs["ID"] = new_logs.index

        if len(old_logs) > 0:
            audit_df['LogDate'] = pd.to_datetime(audit_df['LogDate'])
            old_logs['LogDate'] = pd.to_datetime(old_logs['LogDate'])
            day_diff = (audit_df['LogDate'].max() - old_logs['LogDate'].max()).days
            ts = old_logs['LogDate'].max()
        else:
            day_diff = threshold
            ts = "N/A"
        if day_diff < threshold:
            user_res = input(
                f"The most recent log update is less than {day_diff} days(Timestamp: {ts}). "
                f"Do you want to update logs anyways?(y/n)")
            if user_res.lower() == 'y':
                log_sheet.update(new_logs.values.tolist(), "A2")
                print(f"Update successful. {len(audit_df)} new records inserted to the log.")
            else:
                print("Update aborted. No new records inserted to the log.")
        else:
            log_sheet.update(new_logs.values.tolist(), "A2")
            print(f"Update successful. {len(audit_df)} new records inserted to the log.")


def update_annual_tabs(sh: gspread.spreadsheet.Spreadsheet, audit_df: pd.DataFrame):
    from gspread.exceptions import WorksheetNotFound
    unique_years = audit_df['Year'].drop_duplicates().tolist()

    for y in unique_years:
        print(f"processing {y} transactions...")
        try:
            log_sheet = sh.worksheet(f"{y} logs")
        except WorksheetNotFound:
            print(f"Created new worksheet for {y} logs.")
            log_sheet = sh.add_worksheet(title=f"{y} logs", rows=500, cols=20)

        current_audit = audit_df.loc[audit_df['Year'] == y, :].copy()
        current_audit['ID'] = current_audit.index
        update_log_sheet(log_sheet, current_audit)