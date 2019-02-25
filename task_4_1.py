import argparse


def parse_input(file):
    input_rules_dict = dict()
    with open(file, "r") as file:
        lines = file.readlines()
        lines = [[element.strip() for element in line.replace("\n","").split(":")] for line in lines]
        for line in lines:
            rule_to = [element.strip() for element in line[1].split("|")]
            input_rules_dict[line[0]] = rule_to
    return input_rules_dict

def eliminate_left_recursion(input_rules_map):
    output_rules_map = input_rules_map.copy()

    for rule_index, rule in enumerate(input_rules_map):
        for option_index in range(0, rule_index):
            subsitutions = input_rules_map[rule]
            for sub_index, sub in enumerate(subsitutions):
                sub_array = sub.split(" ")
                terminals = []
                if sub_array[0] == list(input_rules_map.keys())[option_index]:
                    to_rules = input_rules_map[sub_array[0]]
                    for option in to_rules:
                        terminals.append(option + " " + " ".join(sub_array[1:len(sub_array)]))
                    output_rules_map[rule].remove(sub)
                    output_rules_map[rule] = output_rules_map[rule][:sub_index] + terminals + output_rules_map[rule][sub_index:]
            output_rules_map = remove_immediate_self_recursion(rule, output_rules_map)
    return output_rules_map


def remove_immediate_self_recursion(rule, input_rules_map):
    output_rules_map = input_rules_map.copy()
    terminals = []
    non_terminals = []
    for to_rule in input_rules_map[rule]:
        to_rule_array = to_rule.split(" ")
        if to_rule_array[0] == rule:
            new_non_terminal = " ".join(to_rule_array[1:]) + " " + rule + "\'"
            non_terminals.append(new_non_terminal)
        else:
            new_terminal = to_rule + " " + rule+'\''
            terminals.append(new_terminal)
    if len(non_terminals) > 0:
        non_terminals.append("epsilon")
        output_rules_map[rule+'\''] = non_terminals
        output_rules_map[rule] = terminals

    return output_rules_map

def print_output_to_file(input_rules_map, output_file):
    for rule in input_rules_map:
        output_file.write(rule + " : " + " | ".join(input_rules_map[rule]) + "\n")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(add_help=True, description='Sample Commandline')
    parser.add_argument('--file', action="store", help="path of file to take as input", nargs="?", metavar="file")
    args = parser.parse_args()
    output_file = open("task_4_1_result.txt", "w+")

    input_rules_map = parse_input(args.file)
    output = eliminate_left_recursion(input_rules_map)
    # output = remove_immediate_self_recursion(output)

    print_output_to_file(output, output_file)
