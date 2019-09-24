#!/usr/bin/env python3
"""Script to convert DIPS metadata spreadsheets into ArchivesSpace input.
Input is a DIPS formatted CSV spreadsheet. Output is a CSV that uses the
proper header row and fields for upload to ArchivesSpace.
"""

import csv
from os import path
from time import strftime


# TODO: Don't forget to fix Excell spaces with "strip"

def get_file():
    print("Enter the absolute path to the DIPS input CSV.")
    dipsfile = input(" : ")
    print(f"The ArchivesSpace input CSV will be placed in the folder: \n {path.dirname(dipsfile)}")
    print("Please enter the CSV delimiter.")
    delimiter = input(" : ")
    if 't' in delimiter or 'T' in delimiter:
        delimiter = '\t'
    else:
        delimiter = ','
    print(f'Delimiter = \'{delimiter}\' ')
    return dipsfile, delimiter


def convert_file(input_csv, separator):
    """Extracts information from DIPS CSV input and outputs it in ArchivesSpace CSV format.
    ** Aligning metadata fields is done using IF such-and-such IN, but it could be done with IF such-and-such == **
    ** Especially if DIPS field names can be assumed to be STANDARDIZED. The ORDER of the DIPS columns does not matter.
    """
    output_csv = path.join(path.dirname(input_csv), f'as_import_{strftime("%Y%m%d_%H%M%S")}.csv')
    template_header = ['digital_object_id', 'digital_object_language', 'digital_object_script', 'digital_object_level',
                       'digital_object_publish', 'digital_object_type', 'digital_object_restrictions',
                       'digital_object_title', 'digital_object_is_component', 'digital_object_component_id',
                       'agent_role', 'agent_type', 'agent_contact_address_1', 'agent_contact_address_2',
                       'agent_contact_address_3', 'agent_contact_city', 'agent_contact_country', 'agent_contact_email',
                       'agent_contact_fax', 'agent_contact_name', 'agent_contact_post_code', 'agent_contact_region',
                       'agent_contact_salutation', 'agent_contact_telephone', 'agent_contact_telephone_ext',
                       'agent_name_authority_id', 'agent_name_dates', 'agent_name_description_citation',
                       'agent_name_description_note', 'agent_name_description_type', 'agent_name_fuller_form',
                       'agent_name_name_order', 'agent_name_number', 'agent_name_prefix', 'agent_name_primary_name',
                       'agent_name_qualifier', 'agent_name_rest_of_name', 'agent_name_rules', 'agent_name_sort_name',
                       'agent_name_source', 'agent_name_subordinate_name_1', 'agent_name_subordinate_name_2',
                       'agent_name_suffix', 'digital_object_acknowledgement_sent',
                       'digital_object_acknowledgement_sent_date', 'digital_object_agreement_received',
                       'digital_object_agreement_received_date', 'digital_object_agreement_sent',
                       'digital_object_agreement_sent_date', 'digital_object_cataloged',
                       'digital_object_cataloged_date', 'digital_object_cataloged_note', 'digital_object_processed',
                       'digital_object_processed_date', 'digital_object_processing_estimate',
                       'digital_object_processing_hours_total', 'digital_object_processing_plan',
                       'digital_object_processing_priority', 'digital_object_processing_started_date',
                       'digital_object_processing_status', 'digital_object_processing_total_extent',
                       'digital_object_processing_total_extent_type', 'digital_object_processors',
                       'digital_object_rights_determined', 'digital_object_rights_transferred',
                       'digital_object_rights_transferred_date', 'digital_object_rights_transferred_note',
                       'user_defined_boolean_1', 'user_defined_boolean_2', 'user_defined_date_1', 'user_defined_date_2',
                       'user_defined_integer_1', 'user_defined_integer_2', 'user_defined_real_1', 'user_defined_real_2',
                       'user_defined_string_1', 'user_defined_string_2', 'user_defined_string_3', 'user_defined_text_1',
                       'user_defined_text_2', 'user_defined_text_3', 'user_defined_text_4', 'user_defined_text_5',
                       'date_1_begin', 'date_1_end', 'date_1_expression', 'date_1_type', 'date_1_label', 'date_2_begin',
                       'date_2_end', 'date_2_expression', 'date_2_type', 'date_2_label', 'extent_container_summary',
                       'extent_dimensions', 'extent_number', 'extent_physical_details', 'extent_portion', 'extent_type',
                       'subject_source', 'subject_term', 'subject_term_type', 'file_version_file_uri',
                       'file_version_publish', 'file_version_use_statement', 'file_version_xlink_actuate_attribute',
                       'file_version_xlink_show_attribute', 'file_version_file_format_name',
                       'file_version_file_format_version', 'file_version_file_size_bytes', 'file_version_checksum',
                       'file_version_checksum_method']
    with open(input_csv, 'r') as in_csv:
        with open(output_csv, 'w') as out_csv:
            csv_reader = csv.DictReader(in_csv, delimiter=separator)
            dips_headers = csv_reader.fieldnames
            csv_writer = csv.writer(out_csv)
            csv_writer.writerow(template_header)
            num_rows = 0
            for rows in csv_reader:
                blank_row = True
                newrow = []
                for n in range(0, 112):
                    newrow.append("")
                for field in dips_headers:
                    if "identifier" in field.lower():
                        newrow[0] = rows[field]
                        blank_row = False
                    elif "title" in field.lower():
                        newrow[7] = rows[field]
                        blank_row = False
                    elif "language" in field.lower():
                        newrow[1] = rows[field]
                        blank_row = False
                    elif "description" in field.lower():
                        newrow[78] = rows[field]
                        blank_row = False
                    elif "subject" in field.lower():
                        newrow[100] = rows[field]
                        blank_row = False
                    elif "created" in field.lower():
                        newrow[69] = rows[field]
                        blank_row = False
                    elif "type" in field.lower():
                        newrow[5] = rows[field]
                        blank_row = False
                    elif "part" in field.lower():
                        if not rows[field].strip() == "":
                            newrow[3] = "item"
                            blank_row = False
                        else:
                            newrow[3] = "collection"
                    elif "spatial" in field.lower():
                        newrow[75] = rows[field]
                        blank_row = False
                    elif "format" in field.lower():
                        newrow[107] = rows[field]
                        blank_row = False
                if not blank_row:
                    csv_writer.writerow(newrow)
                    num_rows += 1
    print(f'Transformed data from {num_rows} rows.')
    return output_csv


def main():
    dips_csv, delim = get_file()
    aspace_csv = convert_file(dips_csv, delim)
    print(f'Created the ArchivesSpace input file: \n {aspace_csv}')


if __name__ == '__main__':
    main()
