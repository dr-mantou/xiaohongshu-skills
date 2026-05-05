from __future__ import annotations

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from xhs.search import _filter_feeds_by_note_type, _normalize_note_type_filter
from xhs.types import Feed, NoteCard, Video


def _feed(note_type: str, has_video: bool = False) -> Feed:
    return Feed(note_card=NoteCard(type=note_type, video=Video() if has_video else None))


def test_normal_note_type_aliases_cover_text_and_text_image() -> None:
    assert _normalize_note_type_filter("文字+图文") == {"normal"}
    assert _normalize_note_type_filter("text,text+image") == {"normal"}
    assert _normalize_note_type_filter("text and text+image") == {"normal"}
    assert _normalize_note_type_filter("non-video") == {"normal"}


def test_video_and_all_note_type_aliases() -> None:
    assert _normalize_note_type_filter("视频") == {"video"}
    assert _normalize_note_type_filter("video") == {"video"}
    assert _normalize_note_type_filter("不限") is None
    assert _normalize_note_type_filter("normal,video") is None


def test_unknown_note_type_raises_helpful_error() -> None:
    with pytest.raises(ValueError, match="未知 note_type"):
        _normalize_note_type_filter("podcast")


def test_filter_feeds_by_note_type_uses_search_result_kind() -> None:
    feeds = [_feed("normal"), _feed("video"), _feed("", has_video=True), _feed("")]

    normal_feeds = _filter_feeds_by_note_type(feeds, "文字+图文")
    assert normal_feeds == [feeds[0], feeds[3]]

    video_feeds = _filter_feeds_by_note_type(feeds, "视频")
    assert video_feeds == [feeds[1], feeds[2]]
