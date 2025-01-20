from metadatacore.utils.helpers import Helpers
from metadatacore.processors.metadata_processor import MetadataProcessor
from metadatacore.processors.metadata_extractor import MetadataExtractor
from metadatacore.processors.combine_personalization import CombinePersonalization

helper = Helpers()
schema_yml = {
    "registry": helper.read_yaml_file("temp_unzip/dummy_metadata/schema/registry.yml"),
    "assets": {
        "stock_movement": helper.read_yaml_file("temp_unzip/dummy_metadata/schema/assets/stock_movement.yml"),
    },
}
semantics_yml = {
    "registry": helper.read_yaml_file("temp_unzip/dummy_metadata/semantics/registry.yml"),
    "assets": {
        "stock_movement": helper.read_yaml_file("temp_unzip/dummy_metadata/semantics/assets/stock_movement.yml"),
    },
} 
presentation_yml = {"assets": {"file_name": helper.read_yaml_file("temp_unzip/dummy_metadata/presentation/assets/presentation.yml")}}
def combine_metadata():
    processor=MetadataProcessor(schema_yml, semantics_yml)
    final_metrics, final_attributes, final_columns = processor.combine_layers()
    # personalization = CombinePersonalization(final_metrics, final_attributes, final_columns, presentation_yml)
    # final_metrics, final_attributes = personalization.combine_personalizations()
    final_functions = processor.get_all_functions()
    return final_metrics, final_attributes, final_columns, final_functions

def extract_metadata_user_query(query, final_metrics, final_attributes, final_columns, final_functions):
    extractor = MetadataExtractor(final_metrics, final_attributes, final_columns, final_functions)
    extracted_metadata = extractor.extract_metric_and_attribute_from_user_query(query, use_embeddings=False)
    return extracted_metadata