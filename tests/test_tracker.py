import unittest
import warnings
from unittest.mock import patch
import numpy as np
from src.tracker import ShrimpGroupTracker
from src.dataset_parser import DatasetParser

class TrackerTests(unittest.TestCase):
    def setUp(self):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            self.tracker = ShrimpGroupTracker(model_path="missing.pt", min_track_hits=2, max_track_disappeared=1)

    def test_consecutive_confirmation_and_cleanup(self):
        candidate = [(10,10,30,20,.8)]
        self.assertEqual(self.tracker._update_tracks(candidate), [])
        self.assertEqual(len(self.tracker._update_tracks(candidate)), 1)
        self.assertEqual(self.tracker._update_tracks([]), [])
        self.assertEqual(self.tracker._update_tracks(candidate), [])
        self.assertEqual(len(self.tracker._update_tracks(candidate)), 1)
        self.tracker._update_tracks([]); self.tracker._update_tracks([])
        self.assertEqual(self.tracker.shrimp_trajectory_history, {})

    def test_persistent_group_membership_and_reset(self):
        candidates = [(10,10,20,20,.8), (30,10,40,20,.8)]
        frame = np.zeros((80,80,3), dtype=np.uint8)
        with patch.object(self.tracker, "_detect_shrimp_candidates", return_value=candidates):
            self.tracker.update(frame)
            shrimps, groups = self.tracker.update(frame, custom_eps=50, custom_min_samples=2)
            self.assertEqual(len(groups), 1)
            self.assertTrue(all(s.group_id == groups[0].group_id for s in shrimps))
            shrimps, groups = self.tracker.update(frame, custom_eps=5, custom_min_samples=2)
            self.assertEqual(groups, [])
            self.assertTrue(all(s.group_id == -1 for s in shrimps))

    def test_synthetic_metadata_not_aliased(self):
        self.assertEqual(DatasetParser.normalize_video_id("sample_01.mp4"), "sample_01")
        self.assertEqual(DatasetParser.normalize_video_id("Video_08.MP4"), "video_008")
        parser = DatasetParser()
        self.assertFalse(parser.get_dynamic_parameters("sample_01.mp4")["metadata_matched"])
        self.assertTrue(parser.get_dynamic_parameters("video_020.mp4")["metadata_matched"])

if __name__ == "__main__": unittest.main()
