class Relation:
    def __init__(self, columns, data):
        self.columns = columns
        self.data = data

    def __str__(self):
        return str(self.columns) + "\n" + "\n".join(map(str, self.data))

# Get a function to input file
def parse_data_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data_str = file.read()

    data_blocks = data_str.strip().split('{{')  
    relations = {}  # empty data space
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

# The file that we wants to input the data
file_path = 'data.txt'  # You can change to your own file

# get tje data from file
relations,operator = parse_data_file(file_path)


def selection_by_condition(relation, operator, value,col):
    # get the columns and data for searching
    columns = relation.columns
    data = relation.data

    # create a empty list
    selected_data = []
    count1=0
    for i in columns:
        if i ==col:
            
            break
        count1=count1+1
    # go through the rows to find the right one
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

    # create a new relation to return
    selected_relation = Relation(columns, selected_data)

    return selected_relation

def projection(relation, column_names):
    # get the columns and data for searching
    columns = relation.columns
    data = relation.data

    # create a empty list
    projected_data = []

    # get the index for searching
    column_indices = [columns.index(l) for l in column_names]

    # go through
    for row in data:
        projected_row = [row[i] for i in column_indices]
        projected_data.append(projected_row)

    # create a new relation to store the result
    projected_columns = column_names
    projected_relation = Relation(projected_columns, projected_data)

    return projected_relation

def join(relation1, relation2, condition):
    # get the columns and data for searching
    columns1 = relation1.columns
    columns2 = relation2.columns
    data1 = relation1.data
    data2 = relation2.data

    # create a empty list
    joined_data = []

    # get the key for both table
    condition_columns = [col.strip() for col in condition.split('=')]
    left_column = condition_columns[0]
    right_column = condition_columns[1]

    # get the index for both table with the corresponding column
    left_index = columns1.index(left_column)
    right_index = columns2.index(right_column)

    # loop over every element in data1
    for row1 in data1:
        # loop over every elements in data2
        for row2 in data2:
            # if match, create a new row
            if row1[left_index] == row2[right_index]:
                joined_row = row1 + row2
                joined_data.append(joined_row)

    # connect two tables
    joined_columns = columns1 + columns2
    joined_relation = Relation(joined_columns, joined_data)

    return joined_relation




# return the intersection
def intersection(relation1, relation2):
    # get the columns and data for both tables
    columns1 = relation1.columns
    columns2 = relation2.columns
    data1 = relation1.data
    data2 = relation2.data

    # check if them are match 
    if columns1 != columns2:
        raise ValueError("Columns do not match for intersection operation")

    # create a empty list
    intersection_data = []

    # go through every elements in data1
    for row1 in data1:
     # go through every elements in data2
        for row2 in data2:
            if row1 == row2:
                intersection_data.append(row1)
                break

    # create a new relation for result
    intersection_relation = Relation(columns1, intersection_data)

    return intersection_relation

# combine to one relation: Union
def union(relation1, relation2):
    # get the columns and data for both tables
    columns1 = relation1.columns
    columns2 = relation2.columns
    data1 = relation1.data
    data2 = relation2.data

    # check if the columns are fit
    if columns1 != columns2:
        raise ValueError("Columns do not match for union operation")

    # combine to one relation
    union_data = data1 + data2

    # create a new relation for the result
    union_relation = Relation(columns1, union_data)

    return union_relation

def minus(relation1, relation2):
    # get the columns and data for both tables
    columns1 = relation1.columns
    columns2 = relation2.columns
    data1 = relation1.data
    data2 = relation2.data

    # check if the columns are fit
    if columns1 != columns2:
        raise ValueError("Columns do not match for minus operation")

    # get a empty list
    minus_data = []

    # go through every elements in data1
    for row1 in data1:
        # go through every elements in data2
        found_match = False

        # go through every elements in data2 to find if anything matches
        for row2 in data2:
            if row1 == row2:
                found_match = True
                break

        # if nothing matches, update to the result
        if not found_match:
            minus_data.append(row1)

    # create a new relation for the result
    minus_relation = Relation(columns1, minus_data)

    return minus_relation
# show the database
for relation_name, relation in relations.items():
    print(f"{relation_name} Relation:")
    print(relation)




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
  
        for relation_name, rela in relations.items():
            if relation_name == table:
               
                result=selection_by_condition(rela,sign,con,col)
                print("selection:")
                print(result)
                break
    if (operatorL[0].lower()=='projection' or operatorL[0]=='π'):
        col=operatorL[1].replace(' ','').split(',')
        table=operatorL[2].strip("()")
        
  
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
             

            elif relation_name==table2:
                rela2=rela
              
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
           

            elif relation_name==table2:
                rela2=rela

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
            

            elif relation_name==table2:
                rela2=rela
            
        result=minus(rela1, rela2)
        print("Minus Relation:")
        print(result)
        
   
main(relation,operator)