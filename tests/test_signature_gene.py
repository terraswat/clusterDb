
# We don't duplicate tests aready done for common code
# in test_dataset.py and test_clustering_solution.py

import json
import pytest
import tests.access_db_data as ad
from cluster.database.dataset_table import dataset
from cluster.database.clustering_solution_table import clustering_solution
from cluster.database.signature_gene_set_table import signature_gene_set
from cluster.database.signature_gene_table import signature_gene
from cluster.database.db import dicts_equal, merge_dicts

one_data_got_by_parent = merge_dicts(ad.add_one_signature_gene, {})
del(one_data_got_by_parent['signature_gene_set'])
one_data_updated = merge_dicts(ad.add_one_signature_gene, {})
one_data_updated['name'] = 'signature_gene3'
second_data_got_by_parent = merge_dicts(ad.add_second_signature_gene, {})
del(second_data_got_by_parent['signature_gene_set'])


def add_parents():
    dataset.add_one(ad.add_one_dataset)
    clustering_solution.add_one(ad.add_one_clustering_solution)
    signature_gene_set.add_one(ad.add_one_signature_gene_set, ['dataset1'])

def test_add_tsv_and_get_by_parent(app):
    with app.app_context():
        add_parents()
        result = signature_gene.add_tsv('signature_gene.tsv',
            ['signature_gene_set1', 'clustering_solution1', 'dataset1'])
        assert result == 2
        result = signature_gene.get_by_parent(
            ['signature_gene_set1', 'clustering_solution1', 'dataset1'])
        print('result:', result)
        assert result ==  \
'''name
signature_gene1
signature_gene2'''


def test_get_by_parent_parent_not_found(app):
    with app.app_context():
        add_parents()
        signature_gene.add_tsv('signature_gene.tsv',
            ['signature_gene_set1', 'clustering_solution1', 'dataset1'])
        result = signature_gene.get_by_parent(['signature_gene_setX',
            'clustering_solution1', 'dataset1'])
        assert result == \
            '404 Not found: signature_gene_set: signature_gene_setX'


def test_api(client, app):
    # add many tsv
    with app.app_context():
        add_parents()
        response = client.get(
            '/api/signature_gene/add' + \
            '/tsv_file/signature_gene.tsv' + \
            '/signature_gene_set/signature_gene_set1' + \
            '/clustering_solution/clustering_solution1' + \
            '/dataset/dataset1')
        assert response.content_type == ad.text_plain
        assert response.data.decode("utf-8") == '2'

        # get by parent
        response = client.get(
            '/api/signature_gene/get_by' + \
            '/signature_gene_set/signature_gene_set1' + \
            'clustering_solution/clustering_solution1' + \
            '/dataset/dataset1')
        assert response.content_type == ad.text_plain
        print('response.data:', response.data)
        assert response.data.decode("utf-8") == \
'''name
signature_gene1
signature_gene2'''

"""
    # update
    response = client.get('/api/signature_gene/update/name' + \
        '/signature_gene1/field/name/value/signature_gene3')
    assert response.data == b'null\n'
    # check that it was updated
    response = client.get('/api/signature_gene/signature_gene3')
    assert response.content_type == ad.text_plain
    assert response.data.decode("utf-8") == \
'''name	signature_gene_set
signature_gene3	signature_gene_set1'''

    # delete
    response = client.get(
        '/api/signature_gene/delete/signature_gene3')
    assert response.data == b'null\n'
    # check that it was really deleted
    response = client.get('/api/signature_gene/signature_gene3')
    assert response.data.decode("utf-8") == \
        '404 Not found: signature_gene: signature_gene3'
 """

