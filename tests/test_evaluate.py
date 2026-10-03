import unittest
from src.evaluate import evaluate


def doc(boxes, frame=0):
    return {"frames": [{"video_id": "video_001", "frame_index": frame, "boxes": boxes}]}


def box(score=1.0, x=0):
    return {"bbox": [x, 0, x+10, 10], "score": score}


class EvaluationTests(unittest.TestCase):
    def test_duplicate_prediction_is_false_positive(self):
        result = evaluate(doc([box()]), doc([box(.9), box(.8)]))
        self.assertEqual(result["true_positives"], 1)
        self.assertEqual(result["false_positives"], 1)
        self.assertEqual(result["precision"], .5)
        self.assertEqual(result["count_mae"], 1)

    def test_missing_frame_counts_as_missed_detection(self):
        result = evaluate(doc([box()]), {"frames": []})
        self.assertEqual(result["false_negatives"], 1)
        self.assertIsNone(result["precision"])
        self.assertEqual(result["recall"], 0)

    def test_negative_frame_false_positive(self):
        result = evaluate(doc([]), doc([box()]))
        self.assertEqual(result["false_positives"], 1)
        self.assertIsNone(result["recall"])

    def test_confidence_and_iou_thresholds(self):
        result = evaluate(doc([box()]), doc([box(.4), box(.9, 20)]), confidence_threshold=.5)
        self.assertEqual((result["true_positives"], result["false_positives"], result["false_negatives"]), (0,1,1))

    def test_unlabeled_predictions_rejected(self):
        with self.assertRaises(ValueError): evaluate(doc([]), doc([], 1))

    def test_invalid_boxes_and_duplicates_rejected(self):
        for invalid in [box(float("nan")), {"bbox": [0,0,0,1]}, {"bbox": [-1,0,1,1]}]:
            with self.assertRaises(ValueError): evaluate(doc([]), doc([invalid]))
        repeated = doc([]); repeated["frames"] *= 2
        with self.assertRaises(ValueError): evaluate(repeated, doc([]))

    def test_empty_evaluation_rejected(self):
        with self.assertRaises(ValueError): evaluate({"frames": []}, {"frames": []})

if __name__ == "__main__": unittest.main()
