from pypsexec.client import Client


def get_reg_check_actual_value(args_list, ip):

    max_attempts = 5
    for attempt in range(max_attempts):
        try:

            win_client = Client(
                ip[0], username=ip[1], password=ip[2])
            win_client.connect()
            win_client.create_service()

            actual_values = ''
            for arg in args_list:
                stdout, stderr, rc = win_client.run_executable(
                    "powershell.exe", arguments=arg)

                output = stdout.decode("utf-8").replace('\r\n', '')
                actual_values = actual_values + output
            break

        except Exception as e:
            print(f"{ip[0]} | Error: {e}")
            print(f"Tried {attempt+1} times")

        finally:
            win_client.remove_service()
            win_client.disconnect()
            # return actual_values

    actual_value_list = actual_values.split("====")
    actual_value_list.pop(0)
    return actual_value_list


def compare_reg_check(ip_addr, actual_value_list, data_dict):
    # reg check
    df = data_dict["REG_CHECK"]
    checklist_values = df['Checklist'].values
    idx_values = df['Index'].values
    value_data_values = df['Value Data'].values

    result_lists = []

    for idx, val in enumerate(checklist_values):

        pass_result = True

        if val == 1:

            expected_value = str(value_data_values[idx]).lower()

            if actual_value_list[idx] == "":
                actual_value_list[idx] = "Null"

            actual_value = actual_value_list[idx].lower()

            if actual_value == 'null' or actual_value == 'disabled':
                pass_result = True
            else:
                pass_result = False

            if pass_result:
                print(
                    f"{ip_addr} | {idx_values[idx]}: PASSED | Expected: {expected_value} | Actual: {actual_value}")
                result_lists.append("PASSED")
            else:
                print(
                    f"{ip_addr} | {idx_values[idx]}: FAILED | Expected: {expected_value} | Actual: {actual_value}")
                result_lists.append("FAILED")

        else:
            actual_value_list.append("")
            result_lists.append("")

    col_name1 = ip_addr + ' | Actual Value'
    col_name2 = ip_addr + ' | Result'

    df[col_name1] = actual_value_list
    df[col_name2] = result_lists

    return df
