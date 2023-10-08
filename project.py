class Relation:
    def __init__(self, columns, data):
        self.columns = columns
        self.data = data

    def __str__(self):
        return str(self.columns) + "\n" + "\n".join(map(str, self.data))

# 准备一个函数来读取并解析数据文件
def parse_data_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data_str = file.read()

    data_blocks = data_str.strip().split('{{')  # 使用双大括号作为数据块之间的分隔符
    relations = {}  # 用于存储关系的字典
    operator = None

    for data_block in data_blocks:
        lines = data_block.strip().split('\n')
        relation_name = None
        relation_columns = []
        relation_data = []

        for line in lines:
            line = line.strip()

            if line.endswith('{'):  
                relation_name = line.split('=')[0].strip()
                relation_columns = []
                relation_data = []
            
            elif line.startswith('}'):
                relations[relation_name] = Relation(relation_columns, relation_data)
                relation_data = []
            elif relation_name and not relation_columns:
                temp=line.split(',')
                
                for i in temp:
                    relation_columns.append(i.strip())
            elif relation_name and relation_columns:
                line = line.replace(' ', '')
                values = tuple(line.strip().split(','))
                relation_data.append(values)
    
    operator=lines[lines.__len__()-1]
    return relations,operator

# 示例：从文件中读取数据
file_path = 'data.txt'  # 替换为你的数据文件路径

# 解析数据文件
relations,operator = parse_data_file(file_path)


def selection_by_condition(relation, operator, value,col):
    # 获取关系中的列索引
    columns = relation.columns
    data = relation.data

    # 初始化筛选结果
    selected_data = []
    count1=0
    for i in columns:
        if i ==col:
            
            break
        count1=count1+1
    # 遍历关系中的每个元组
    for row in data:
        count2=0
        for element in row:
            
            if operator == "=" and element == value and count1==count2:
                selected_data.append(row)
            elif operator == ">" and element > value and count1==count2:
                selected_data.append(row)
            elif operator == "<" and element < value and count1==count2:
                selected_data.append(row)
            elif operator == "≠" and element != value and count1==count2:
                selected_data.append(row)
            elif operator == "≥" and element >= value and count1==count2:
                selected_data.append(row)
            elif operator == "≤" and element <= value and count1==count2:
                selected_data.append(row)
            count2=count2+1

    # 创建新的关系对象来存储筛选结果
    selected_relation = Relation(columns, selected_data)

    return selected_relation

def projection(relation, column_names):
    # 获取关系中的列索引
    columns = relation.columns
    data = relation.data

    # 初始化投影结果
    projected_data = []

    # 获取列索引列表
    column_indices = [columns.index(l) for l in column_names]

    # 遍历关系中的每个元组，只保留指定的列
    for row in data:
        projected_row = [row[i] for i in column_indices]
        projected_data.append(projected_row)

    # 创建新的关系对象来存储投影结果
    projected_columns = column_names
    projected_relation = Relation(projected_columns, projected_data)

    return projected_relation

def join(relation1, relation2, condition):
    # 获取关系1和关系2的列索引
    columns1 = relation1.columns
    columns2 = relation2.columns
    data1 = relation1.data
    data2 = relation2.data

    # 初始化连接结果
    joined_data = []

    # 获取连接条件中的列索引
    condition_columns = [col.strip() for col in condition.split('=')]
    left_column = condition_columns[0]
    right_column = condition_columns[1]

    # 获取左关系和右关系中的连接列索引
    left_index = columns1.index(left_column)
    right_index = columns2.index(right_column)

    # 遍历左关系的每个元组
    for row1 in data1:
        # 遍历右关系的每个元组
        for row2 in data2:
            # 如果连接条件匹配，将两个元组合并成一个新元组
            if row1[left_index] == row2[right_index]:
                joined_row = row1 + row2
                joined_data.append(joined_row)

    # 创建新的关系对象来存储连接结果
    joined_columns = columns1 + columns2
    joined_relation = Relation(joined_columns, joined_data)

    return joined_relation




# 交集操作：返回两个关系的交集结果
def intersection(relation1, relation2):
    # 获取关系1和关系2的列索引
    columns1 = relation1.columns
    columns2 = relation2.columns
    data1 = relation1.data
    data2 = relation2.data

    # 检查列是否匹配
    if columns1 != columns2:
        raise ValueError("Columns do not match for intersection operation")

    # 初始化交集结果
    intersection_data = []

    # 遍历关系1的每个元组
    for row1 in data1:
        # 遍历关系2的每个元组，检查是否有匹配的元组
        for row2 in data2:
            if row1 == row2:
                intersection_data.append(row1)
                break

    # 创建新的关系对象来存储交集结果
    intersection_relation = Relation(columns1, intersection_data)

    return intersection_relation

# 并集操作：将两个关系合并为一个新的关系
def union(relation1, relation2):
    # 获取关系1和关系2的列索引
    columns1 = relation1.columns
    columns2 = relation2.columns
    data1 = relation1.data
    data2 = relation2.data

    # 检查列是否匹配
    if columns1 != columns2:
        raise ValueError("Columns do not match for union operation")

    # 合并关系数据
    union_data = data1 + data2

    # 创建新的关系对象来存储并集结果
    union_relation = Relation(columns1, union_data)

    return union_relation

def minus(relation1, relation2):
    # 获取关系1和关系2的列索引
    columns1 = relation1.columns
    columns2 = relation2.columns
    data1 = relation1.data
    data2 = relation2.data

    # 检查列是否匹配
    if columns1 != columns2:
        raise ValueError("Columns do not match for minus operation")

    # 初始化差集结果
    minus_data = []

    # 遍历关系1的每个元组
    for row1 in data1:
        # 标志是否在关系2中找到匹配的元组
        found_match = False

        # 遍历关系2的每个元组，检查是否有匹配的元组
        for row2 in data2:
            if row1 == row2:
                found_match = True
                break

        # 如果没有找到匹配的元组，将关系1的元组添加到差集结果中
        if not found_match:
            minus_data.append(row1)

    # 创建新的关系对象来存储差集结果
    minus_relation = Relation(columns1, minus_data)

    return minus_relation
# 显示结果
for relation_name, relation in relations.items():
    print(f"{relation_name} Relation:")
    print(relation)

print(operator.split())


def main(re,op):
    operatorL=operator.split()
    if(operatorL[0].lower()=='select' or operatorL[0]=="σ"):
        sign=None
        table=operatorL[2].strip("()")
        col=None
        con=None
        count=0
        
        for i in operatorL[1]:
            if i =='>' or i == "<" or i=="=" or i =="≠" or i =="≥" or i =="≤":
                sign=i
               
                col=operatorL[1][:count]
                con=operatorL[1][count+1:] 
                break
            count=count+1
        print(table,sign,con,col)
        for relation_name, rela in relations.items():
            if relation_name == table:
                print(rela)
                result=selection_by_condition(rela,sign,con,col)
                print("selection:")
                print(result)
                break
    if (operatorL[0].lower()=='projection' or operatorL[0]=='π'):
        col=operatorL[1].replace(' ','').split(',')
        table=operatorL[2].strip("()")
        
        print(col,table)
        for relation_name, rela in relations.items():
            if relation_name == table:
                
                result=projection(rela,col)
                print("projection:")
                print(result)
                break
    if(operatorL[1]=="⨝" or operatorL[1].lower()=="join"):
        table1=operatorL[0].strip("()")
        table2=operatorL[3].strip("()")
        con=operatorL[2]
        rela1=None
        rela2=None
        for relation_name, rela in relations.items():
            if relation_name == table1:
                rela1=rela

            elif relation_name==table2:
                rela2=rela

        result=join(rela1, rela2, con)
        print("join:")
        print(result)
        
    if (operatorL[1]=='∪' or operatorL[1].lower()=='union'):
        table1=operatorL[0].strip("()")
        table2=operatorL[2].strip("()")
        rela1=None
        rela2=None
        #print(table1,table2)
        for relation_name, rela in relations.items():
            if relation_name == table1:
                rela1=rela
                print(rela1)

            elif relation_name==table2:
                rela2=rela
                print(rela2)
        result=union(rela1, rela2)
        print("Union Relation:")
        print(result)
        
        
        
    if (operatorL[1]=='∩' or operatorL[1].lower()=='intersection'):
        table1=operatorL[0].strip("()")
        table2=operatorL[2].strip("()")
        rela1=None
        rela2=None
        #print(table1,table2)
        for relation_name, rela in relations.items():
            if relation_name == table1:
                rela1=rela
                print(rela1)

            elif relation_name==table2:
                rela2=rela
                print(rela2)
        result=intersection(rela1, rela2)
        print("Intersection Relation:")
        print(result)
        
    if (operatorL[1]=='-' or operatorL[1].lower()=='minus'):
        table1=operatorL[0].strip("()")
        table2=operatorL[2].strip("()")
        rela1=None
        rela2=None
        #print(table1,table2)
        for relation_name, rela in relations.items():
            if relation_name == table1:
                rela1=rela
                print(rela1)

            elif relation_name==table2:
                rela2=rela
                print(rela2)
        result=minus(rela1, rela2)
        print("Minus Relation:")
        print(result)
        
   
main(relation,operator)