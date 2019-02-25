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


def eliminate_left_factoring(input_rules_map):
    output_rules_map = input_rules_map.copy()
    for rule_index, rule in enumerate(input_rules_map):
        left_factors_elements = []
        non_left_factors_elements = []
        for to_rule in input_rules_map[rule]:
            to_rule_array = to_rule.split(" ")
            if to_rule_array[0] == rule:
                left_factor_element = " ".join(to_rule_array[1:])
                left_factors_elements.append(left_factor_element)
            else:
                non_left_factor_element = to_rule
                non_left_factors_elements.append(non_left_factor_element)

        non_left_factors_elements = [rule +" " + rule + "\'"] + non_left_factors_elements
        output_rules_map[rule] = non_left_factors_elements
        output_rules_map[rule+'\''] = left_factors_elements
    return output_rules_map

def print_output_to_file(input_rules_map, output_file):
    for rule in input_rules_map:
        output_file.write(rule + " : " + " | ".join(input_rules_map[rule]) + "\n")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(add_help=True, description='Sample Commandline')
    parser.add_argument('--file', action="store", help="path of file to take as input", nargs="?", metavar="file")
    args = parser.parse_args()
    output_file = open("task_4_2_result.txt", "w+")

    input_rules_map = parse_input(args.file)
    output = eliminate_left_factoring(input_rules_map)

    print_output_to_file(output, output_file)
