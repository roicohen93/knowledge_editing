from benchmark import Dataset, Example, TestsAxis


def len_of_each_axis(example: Example):
    res_dict = dict()
    example_dict = example.to_dict()
    for axis in TestsAxis:
        axis_name = axis.name.lower()
        if axis_name == 'previous_storage':
            axis_name = 'prev_storage'
        if axis_name != 'logical_constraints':
            axis_name += '_tests'
        res_dict[axis_name] = len(example_dict[axis_name])
    return res_dict


dataset_path = './benchmark/top_views_1000.json'
dataset = Dataset.from_file(dataset_path)

if __name__ == '__main__':
    print(len(dataset.examples))
    # print(dataset.examples[0])
    # print(dataset.examples[0].to_dict())
    for i, example in enumerate(dataset.examples):
        print(len_of_each_axis(example))
        if i > 20:
            break
