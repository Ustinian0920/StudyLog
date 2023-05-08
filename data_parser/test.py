
from swtree import *







afile_mapper = SWMapper()
afile_yaml_path = "/home/lianke/swswf/framework/mappers/onetwo_ids_mapper.yaml"
afile_mapper.updateMapperYAMLFile(afile_yaml_path)
afile_tree = afile_mapper.ids_reflect_mapping("iter",123,0,10)
afile_data = afile_tree.toDict()

print(afile_data)