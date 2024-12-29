from typing import List, Tuple
from structs import Node, Element


def read_file(file_name: str) -> Tuple[List[Element], List[Node], List[int]]:
    """
    Reads the input file and parses nodes, elements, and field values

    Args:
        file_name (str): path to the input file

    Returns:
        Tuple[List[Element], List[Node], List[int]]:
            - elements: List of parsed Element objects.
            - nodes: List of parsed Node objects.
            - field_values: List of field values (temperature, density, etc.)
    """

    elements, nodes, field_values = [], [], []

    with open(file_name, 'r') as file:
        current_section = None

        for line in file:
            stripped_line = line.strip()

            if stripped_line.startswith("*Node"):
                current_section = 'nodes'
                continue
            elif stripped_line.startswith("*Element,"):
                current_section = 'elements'
                continue
            elif stripped_line.startswith("*BC"):
                current_section = 'boundary_conditions'
                continue

            if current_section == 'elements':
                element = parse_element_line(stripped_line)
                elements.append(element)
            elif current_section == 'nodes':
                node = parse_node_line(stripped_line)
                nodes.append(node)
            elif current_section == 'boundary_conditions':
                parse_boundary_conditions_line(stripped_line, nodes)
            else:
                field_values.append(parse_field_value_line(stripped_line))

    return elements, nodes, field_values


def parse_node_line(line: str) -> Node:
    """Parses a single line in the node section."""
    parts = [float(x.replace(',', '')) for x in line.split()]
    return Node(parts[1], parts[2])


def parse_element_line(line: str) -> Element:
    """Parses a single line in the element section."""
    parts = [int(x.replace(',', '')) for x in line.split()]
    return Element(parts[1:5])


def parse_boundary_conditions_line(line: str, nodes: List[Node]) -> None:
    """Parses boundary condition lines and updates nodes."""
    bc_nodes = [int(val.replace(',', '')) - 1 for val in line.split()]
    for i, node in enumerate(nodes):
        if i in bc_nodes:
            node.BC = True


def parse_field_value_line(line: str) -> int:
    """Parses a line with other numerical data."""
    parts = [x for x in line.split() if x]
    return int(parts[-1])
