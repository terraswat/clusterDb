
# We don't duplicate tests aready done for common code
# in test_dataset.py and test_clustering_solution.py

import pytest
import tests.access_db_data as ad
from cluster.database.dataset_table import dataset
from cluster.database.clustering_solution_table import clustering_solution
from cluster.database.signature_gene_set_table import signature_gene_set
from cluster.database.signature_gene_table import signature_gene
from cluster.database.db import dicts_equal, merge_dicts

one_data_got = merge_dicts(ad.add_one_signature_gene_set, {})
del(one_data_got['clustering_solution'])
one_data_added = merge_dicts(ad.add_one_signature_gene_set, {'clustering_solution_id': 1})
del(one_data_added['clustering_solution'])

second_data_got = merge_dicts(ad.add_second_signature_gene_set, {})
del(second_data_got['clustering_solution'])
second_data_added = merge_dicts(ad.add_second_signature_gene_set, {'clustering_solution_id': 1})
del(second_data_added['clustering_solution'])


def add_parents():
    dataset.add_one(ad.add_one_dataset)
    clustering_solution.add_one(ad.add_one_clustering_solution)


def test_add_one(app):
    with app.app_context():
        add_parents()
        result = signature_gene_set.add_one(ad.add_one_signature_gene_set)
        assert result == None
        result = signature_gene_set.get_one(
            'signature_gene_set1', ad.accept_json)
        assert dicts_equal(result, one_data_added)


def test_add_one_parent_not_found(app):
    with app.app_context():
        result = signature_gene_set.add_one(ad.add_one_signature_gene_set)
        assert result == \
            '404 Parent not found: clustering_solution: clustering_solution1'


def test_delete_has_children(app):
    with app.app_context():
        add_parents()
        signature_gene_set.add_one(ad.add_one_signature_gene_set)
        signature_gene.add_one(ad.add_one_signature_gene)
        result = signature_gene_set.delete('signature_gene_set1')
        assert result == \
            '400 There are children that would be orphaned, delete them first'


def test_get_by_parent_one(app):
    with app.app_context():
        add_parents()
        signature_gene_set.add_one(ad.add_one_signature_gene_set)
        result = signature_gene_set.get_by_parent('clustering_solution1', ad.accept_json)
        assert dicts_equal(result[0], one_data_got)


def test_get_by_parent_parent_not_found(app):
    with app.app_context():
        add_parents()
        signature_gene_set.add_one(ad.add_one_signature_gene_set)
        result = signature_gene_set.get_by_parent('clustering_solutionX', ad.accept_json)
        assert result == '404 Parent not found: clustering_solution: clustering_solutionX'


def test_get_one(app):
    with app.app_context():
        add_parents()
        signature_gene_set.add_one(ad.add_one_signature_gene_set)
        result = signature_gene_set.get_one('signature_gene_set1', ad.accept_json)
        assert dicts_equal(result, one_data_added)
