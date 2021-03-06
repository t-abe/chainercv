import unittest
import warnings

import numpy as np

from chainer import cuda
from chainer import testing
from chainer.testing import attr


from chainercv.evaluations import eval_semantic_segmentation


@testing.parameterize(
    # p_00 = 2
    # p_01 = 1
    # p_10 = 0
    # p_11 = 2
    {'pred_labels': [[[1, 1, 0], [0, 0, 1]]],
     'gt_labels': [[[1, 0, 0], [0, -1, 1]]],
     'acc': [4. / 5.],
     'acc_cls': [1. / 2. * (1. + 2. / 3.)],
     'mean_iou': [1. / 2. * (1. / 3. + 1.)],
     'fwavacc': [1. / 5. * (2. + 4. / 3.)]
     },
    {'pred_labels': np.repeat([[[1, 1, 0], [0, 0, 1]]], 2, axis=0),
     'gt_labels': np.repeat([[[1, 0, 0], [0, -1, 1]]], 2, axis=0),
     'acc': [4. / 5., 4. / 5.],
     'acc_cls': [1. / 2. * (1. + 2. / 3.),
                 1. / 2. * (1. + 2. / 3.)],
     'mean_iou': [1. / 2. * (1. / 3. + 1.),
                  1. / 2. * (1. / 3. + 1.)],
     'fwavacc': [1. / 5. * (2. + 4. / 3.),
                 1. / 5. * (2. + 4. / 3.)]
     },
    {'pred_labels': [[[0, 0, 0], [0, 0, 0]]],
     'gt_labels': [[[1, 1, 1], [1, 1, 1]]],
     'acc': [0.],
     'acc_cls': [0.],
     'mean_iou': [0.],
     'fwavacc': [0.]
     }
)
class TestEvalSemanticSegmentation(unittest.TestCase):

    n_class = 2

    def check_eval_semantic_segmentation(self, pred_labels, gt_labels, acc,
                                         acc_cls, mean_iou, fwavacc, n_class):
        with warnings.catch_warnings(record=True) as w:
            acc_o, acc_cls_o, mean_iou_o, fwavacc_o =\
                eval_semantic_segmentation(
                    pred_labels, gt_labels, n_class=n_class)

        self.assertIsInstance(acc_o, type(acc))
        self.assertIsInstance(acc_cls_o, type(acc_cls))
        self.assertIsInstance(mean_iou_o, type(mean_iou))
        self.assertIsInstance(fwavacc_o, type(fwavacc))

        np.testing.assert_equal(cuda.to_cpu(acc_o), cuda.to_cpu(acc))
        np.testing.assert_equal(cuda.to_cpu(acc_cls_o), cuda.to_cpu(acc_cls))
        np.testing.assert_equal(cuda.to_cpu(mean_iou_o), cuda.to_cpu(mean_iou))
        np.testing.assert_equal(cuda.to_cpu(fwavacc_o), cuda.to_cpu(fwavacc))

        # test that no warning has been created
        self.assertEqual(len(w), 0)

    def test_eval_semantic_segmentation_cpu(self):
        self.check_eval_semantic_segmentation(
            np.array(self.pred_labels),
            np.array(self.gt_labels),
            np.array(self.acc),
            np.array(self.acc_cls),
            np.array(self.mean_iou),
            np.array(self.fwavacc),
            self.n_class)

    @attr.gpu
    def test_eval_semantic_segmentation_gpu(self):
        self.check_eval_semantic_segmentation(
            cuda.cupy.array(self.pred_labels),
            cuda.cupy.array(self.gt_labels),
            cuda.cupy.array(self.acc),
            cuda.cupy.array(self.acc_cls),
            cuda.cupy.array(self.mean_iou),
            cuda.cupy.array(self.fwavacc),
            self.n_class)


class TestEvalSemanticSegmentationListInput(unittest.TestCase):

    n_class = 2

    def setUp(self):
        self.pred_labels = np.array([[1, 1, 0], [0, 0, 1]])
        self.gt_labels = np.array([[1, 0, 0], [0, -1, 1]])
        self.acc = np.repeat([4. / 5.], 2)
        self.acc_cls = np.repeat([1. / 2. * (1. + 2. / 3.)], 2)
        self.mean_iou = np.repeat([1. / 2. * (1. / 3. + 1)], 2)
        self.fwavacc = np.repeat([1. / 5. * (2. + 4. / 3.)], 2)

    def check_eval_semantic_segmentation_list_input(
            self, pred_labels, gt_labels, acc,
            acc_cls, mean_iou, fwavacc, n_class):
        with warnings.catch_warnings(record=True) as w:
            acc_o, acc_cls_o, mean_iou_o, fwavacc_o =\
                eval_semantic_segmentation(
                    pred_labels, gt_labels, n_class=n_class)

        self.assertIsInstance(acc_o, type(acc))
        self.assertIsInstance(acc_cls_o, type(acc_cls))
        self.assertIsInstance(mean_iou_o, type(mean_iou))
        self.assertIsInstance(fwavacc_o, type(fwavacc))

        np.testing.assert_equal(cuda.to_cpu(acc_o), cuda.to_cpu(acc))
        np.testing.assert_equal(cuda.to_cpu(acc_cls_o), cuda.to_cpu(acc_cls))
        np.testing.assert_equal(cuda.to_cpu(mean_iou_o), cuda.to_cpu(mean_iou))
        np.testing.assert_equal(cuda.to_cpu(fwavacc_o), cuda.to_cpu(fwavacc))

        # test that no warning has been created
        self.assertEqual(len(w), 0)

    def test_eval_semantic_segmentation_list_input_cpu(self):
        self.check_eval_semantic_segmentation_list_input(
            [self.pred_labels, self.pred_labels],
            [self.gt_labels, self.gt_labels],
            self.acc, self.acc_cls, self.mean_iou, self.fwavacc, self.n_class)

    @attr.gpu
    def test_eval_semantic_segmentation_list_input_gpu(self):
        self.check_eval_semantic_segmentation_list_input(
            [cuda.to_gpu(self.pred_labels), cuda.to_gpu(self.pred_labels)],
            [cuda.to_gpu(self.gt_labels), cuda.to_gpu(self.gt_labels)],
            cuda.to_gpu(self.acc), cuda.to_gpu(self.acc_cls),
            cuda.to_gpu(self.mean_iou), cuda.to_gpu(self.fwavacc),
            self.n_class)


testing.run_module(__name__, __file__)
