import unittest

from unittest.mock import patch
from canonicalwebteam.blog.common_view_logic import (
    get_index_context,
    get_article_context,
)
from canonicalwebteam.blog import wordpress_api as api


class TestCommonViewLogic(unittest.TestCase):
    @patch("canonicalwebteam.blog.wordpress_api.get_group_by_id")
    @patch("canonicalwebteam.blog.wordpress_api.get_category_by_id")
    @patch("canonicalwebteam.blog.wordpress_api.get_user")
    @patch("canonicalwebteam.blog.wordpress_api.get_media")
    def test_building_index_context(
        self, get_media, get_user, get_category_by_id, get_group_by_id
    ):
        get_media.return_value = "test_image"
        get_user.return_value = "test_author"
        get_category_by_id.return_value = "test_category"
        get_group_by_id.return_value = "test_group"
        articles = [
            {
                "featured_media": "test",
                "author": "test",
                "categories": [1, 2],
                "group": [1],
                "tags": ["test"],
            },
            {
                "featured_media": "test2",
                "author": "test2",
                "categories": [2, 3],
                "group": [1],
                "tags": ["test2"],
            },
        ]
        context = get_index_context(1, articles, 2)
        expected_context = {
            "current_page": 1,
            "total_pages": 2,
            "articles": [
                {
                    "author": "test_author",
                    "categories": [1, 2],
                    "featured_media": "test",
                    "group": 1,
                    "image": "test_image",
                    "tags": ["test"],
                },
                {
                    "author": "test_author",
                    "categories": [2, 3],
                    "featured_media": "test2",
                    "group": 1,
                    "image": "test_image",
                    "tags": ["test2"],
                },
            ],
            "groups": {1: "test_group"},
            "used_categories": {
                1: "test_category",
                2: "test_category",
                3: "test_category",
            },
        }
        self.assertEqual(context, expected_context)

    def test_building_index_context_without_api(self):
        articles = [
            {
                "featured_media": "test",
                "author": "test",
                "categories": [1, 2],
                "group": [1],
                "tags": ["test"],
            },
            {
                "featured_media": "test2",
                "author": "test2",
                "categories": [2, 3],
                "group": [1],
                "tags": ["test2"],
            },
        ]
        context = get_index_context(1, articles, 2)
        expected_context = {
            "current_page": 1,
            "total_pages": 2,
            "articles": [
                {
                    "author": None,
                    "categories": [1, 2],
                    "featured_media": "test",
                    "group": 1,
                    "image": None,
                    "tags": ["test"],
                },
                {
                    "author": None,
                    "categories": [2, 3],
                    "featured_media": "test2",
                    "group": 1,
                    "image": None,
                    "tags": ["test2"],
                },
            ],
            "groups": {1: None},
            "used_categories": {1: None, 2: None, 3: None},
        }
        self.assertEqual(context, expected_context)

    @patch("canonicalwebteam.blog.wordpress_api.get_tags_by_ids")
    @patch("canonicalwebteam.blog.wordpress_api.get_articles")
    @patch("canonicalwebteam.blog.wordpress_api.get_user")
    @patch("canonicalwebteam.blog.wordpress_api.get_media")
    def test_building_article_context(
        self, get_media, get_user, get_articles, get_tags_by_id
    ):
        get_media.return_value = "test_image"
        get_articles.return_value = (
            [
                {
                    "id": 2,
                    "featured_media": "test_related_article_image",
                    "author": "test_related_article_author",
                    "categories": [4, 5],
                    "group": [4],
                    "tags": ["test_related_article"],
                }
            ],
            2,
        )
        get_user.return_value = "test_author"
        get_tags_by_id.return_value = [
            {"id": 1, "name": "test_tag_1"},
            {"id": 2, "name": "test_tag_2"},
        ]
        articles = [
            {
                "id": 1,
                "featured_media": "test",
                "author": "test",
                "categories": [1, 2],
                "group": [1],
                "tags": ["test"],
            }
        ]
        context = get_article_context(articles)
        expected_context = {
            "article": {
                "id": 1,
                "author": "test_author",
                "categories": [1, 2],
                "featured_media": "test",
                "group": 1,
                "image": None,
                "tags": ["test"],
            },
            "is_in_series": False,
            "related_articles": [
                {
                    "id": 2,
                    "featured_media": "test_related_article_image",
                    "author": None,
                    "categories": [4, 5],
                    "group": 4,
                    "image": None,
                    "tags": ["test_related_article"],
                }
            ],
            "tags": [
                {"id": 1, "name": "test_tag_1"},
                {"id": 2, "name": "test_tag_2"},
            ],
        }

        self.assertEqual(context, expected_context)

    def test_building_article_context_without_api(self):
        articles = [
            {
                "id": 1,
                "featured_media": "test",
                "author": "test",
                "categories": [1, 2],
                "group": [1],
                "tags": ["test"],
            }
        ]
        context = get_article_context(articles)
        expected_context = {
            "article": {
                "id": 1,
                "author": None,
                "categories": [1, 2],
                "featured_media": "test",
                "group": 1,
                "image": None,
                "tags": ["test"],
            },
            "is_in_series": False,
            "related_articles": None,
            "tags": [],
        }

        self.maxDiff = None
        self.assertEqual(context, expected_context)
