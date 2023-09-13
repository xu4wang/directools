from directus_sdk import DirectusClient_V9
from config import get_config
import json
import os

config_obj = get_config()

print(config_obj)

# Create a directus client connection with user static token
client = DirectusClient_V9(url=config_obj['directus']['url'], token=config_obj['directus']['token'])

def add_operations_to_flows(flows, operations):
    # 创建一个字典，用于存储operations的id和对应的operations对象
    operations_dict = {operation["id"]: operation for operation in operations}

    # 遍历flows列表，查找每个flow中的operations，并替换为对应的operations对象
    for flow in flows:
        flow_operations = flow.get("operations", [])  # 获取当前flow的operations列表
        operations_objs = []  # 用于存储对应的operations对象

        # 根据flow的operations列表，查找对应的operations对象
        for operation_id in flow_operations:
            if operation_id in operations_dict:
                operations_objs.append(operations_dict[operation_id])

        # 将对应的operations对象存储在flow中的operations_obj键中
        flow["operations_obj"] = operations_objs.copy()

    return flows

def add_permissions_to_roles(roles, permissions):

    # 遍历roles列表，查找每个role中的permissions，并替换为对应的permissions对象
    for role in roles:
        permissions_objs = []  # 用于存储对应的permissions对象

        # 根据role的permissions列表，查找对应的permissions对象
        for permission in permissions:
            if permission['role'] == role['id']:
                permissions_objs.append(permission)

        # 将对应的permissions对象存储在role中的permissions_obj键中
        role["permissions_obj"] = permissions_objs.copy()

    return roles

def save_roles_to_files(roles, directory):
    # 创建保存目录（如果不存在）
    if not os.path.exists(directory):
        os.makedirs(directory)

    # 遍历roles列表，将每个role保存到对应的文件中
    for role in roles:
        file_name = f"{role['name']}.json"  # 使用role.name作为文件名
        file_path = os.path.join(directory, file_name)  # 拼接文件路径

        # 将role对象转换为JSON格式的字符串
        formatted_json = json.dumps(role, ensure_ascii=False, indent=4)

        # 将JSON字符串写入文件
        with open(file_path, 'w') as file:
            file.write(formatted_json)

        print(f"Role '{role['name']}' saved to file: {file_path}")

def save_flows_to_files(flows, directory):
    # 创建保存目录（如果不存在）
    if not os.path.exists(directory):
        os.makedirs(directory)

    # 遍历flows列表，将每个flow保存到对应的文件中
    for flow in flows:
        file_name = f"{flow['name']}.json"  # 使用flow.name作为文件名
        file_path = os.path.join(directory, file_name)  # 拼接文件路径

        # 将flow对象转换为JSON格式的字符串
        formatted_json = json.dumps(flow, ensure_ascii=False, indent=4)

        # 将JSON字符串写入文件
        with open(file_path, 'w') as file:
            file.write(formatted_json)

        print(f"Flow '{flow['name']}' saved to file: {file_path}")


def restore_flows_from_files(directory):
    flows = []

    # 遍历目录中的所有文件
    for file_name in os.listdir(directory):
        file_path = os.path.join(directory, file_name)

        # 仅处理以 .json 结尾的文件
        if file_name.endswith(".json"):
            # 读取文件中的JSON数据
            with open(file_path, 'r') as file:
                flow_data = file.read()

            # 解析JSON数据并添加到flows列表
            flow = json.loads(flow_data)
            flows.append(flow)

    return flows

def restore_roles_from_files(directory):
    roles = []

    # 遍历目录中的所有文件
    for file_name in os.listdir(directory):
        file_path = os.path.join(directory, file_name)

        # 仅处理以 .json 结尾的文件
        if file_name.endswith(".json"):
            # 读取文件中的JSON数据
            with open(file_path, 'r') as file:
                role_data = file.read()

            # 解析JSON数据并添加到roles列表
            role = json.loads(role_data)
            roles.append(role)

    return roles

def sort_dependency_array(operations):
    sorted_operations = []
    visited = set()  # 用于跟踪已访问的操作

    def dfs(operation):
        visited.add(operation["id"])
        for dependency_id in [operation.get("resolve"), operation.get("reject")]:
            if dependency_id and dependency_id not in visited:
                dependency = next((op for op in operations if op["id"] == dependency_id), None)
                if dependency:
                    dfs(dependency)
        sorted_operations.append(operation)

    for operation in operations:
        if operation["id"] not in visited:
            dfs(operation)

    #sorted_operations.reverse()  # 反转列表，以得到正确的顺序
    return sorted_operations

def save_roles():
    roles = client.get(f"/roles")

    #remove role if role.name == "Administrator"
    roles = [role for role in roles if role['name'] != "Administrator"]

    permissions = client.get(f"/permissions")
    roles = add_permissions_to_roles(roles, permissions)
    directory = config_obj['system']['folder'] + "/roles"
    if roles:
        save_roles_to_files(roles, directory)
    else:
        print("No roles found!")


def save_flows():
    flows = client.get(f"/flows", params={"limit": "10000"})
    print(len(flows))
    operations = client.get(f"/operations", params={"limit": "10000"})
    print(len(operations))
    flows = add_operations_to_flows(flows, operations)
    directory = config_obj['system']['folder'] + "/flows"
    if flows:
        save_flows_to_files(flows, directory)
    else:
        print("No flows found!")

def load_roles():
    directory = config_obj['system']['folder'] + "/roles"
    roles = restore_roles_from_files(directory)
    if roles:
        for role in roles:
            print("Loading "+role['name'])
            permissions = role['permissions_obj']
            del role['permissions_obj']
            #delete role if it's already there
            try:
                client.delete(f"/roles/{role['id']}")
            except:
                pass
            client.post(f"/roles", json=role)

            #delete permissions for the role if they're already there
            for permission in permissions:
                try:
                    client.delete(f"/permissions/{permission['id']}")
                except:
                    pass

            #add permissions to role
            for permission in permissions:
                client.post(f"/permissions", json=permission)

def load_flow( name ):
    directory = config_obj['system']['folder'] + "/flows"
    flows = restore_flows_from_files(directory)
    if flows:
        for flow in flows:
            if flow['name'] == name:
                print("Loading "+flow['name'])
                operations = flow['operations_obj']
                
                # "operation": null,
                #"date_created": "2023-07-12T05:55:44",
                #"user_created": "0a743283-dd90-4c7f-a13c-96c41d071e74",
                #"operations": [],
                #"operations_obj": []
                #
                #del flow['operation']
                del flow['date_created']
                del flow['user_created']
                del flow['operations']
                del flow['operations_obj']

                #delete flow if it's already there
                try:
                    client.delete(f"/flows/{flow['id']}")
                except:
                    pass
                client.post(f"/flows", json=flow)

                #print("Operations:")
                #print(json.dumps(operations, indent=4))

                sorted_operations = sort_dependency_array(operations)

                # 请把sorted_operations  格式化后打印出来

                #print("Sorted Operations:")
                #print(json.dumps(sorted_operations, indent=4))

                for operation in sorted_operations:
                    #delete operation if it's already there
                    try:
                        client.delete(f"/operations/{operation['id']}")
                        del operation['date_created']
                        del operation['user_created']
                    except:
                        pass
                    client.post(f"/operations", json=operation)

    else:  
        print("No flows found!")
  
def load_flows():
    directory = config_obj['system']['folder'] + "/flows"
    flows = restore_flows_from_files(directory)
    if flows:
        for flow in flows:
            print("Loading "+flow['name'])
            operations = flow['operations_obj']
            
            # "operation": null,
            #"date_created": "2023-07-12T05:55:44",
            #"user_created": "0a743283-dd90-4c7f-a13c-96c41d071e74",
            #"operations": [],
            #"operations_obj": []
            #
            #del flow['operation']
            del flow['date_created']
            del flow['user_created']
            del flow['operations']
            del flow['operations_obj']

            #delete flow if it's already there
            try:
                client.delete(f"/flows/{flow['id']}")
            except:
                pass
            client.post(f"/flows", json=flow)

            #print("Operations:")
            #print(json.dumps(operations, indent=4))

            sorted_operations = sort_dependency_array(operations)

            # 请把sorted_operations  格式化后打印出来

            #print("Sorted Operations:")
            #print(json.dumps(sorted_operations, indent=4))

            for operation in sorted_operations:
                #delete operation if it's already there
                try:
                    client.delete(f"/operations/{operation['id']}")
                    del operation['date_created']
                    del operation['user_created']
                except:
                    pass
                client.post(f"/operations", json=operation)

    else:  
        print("No flows found!")
