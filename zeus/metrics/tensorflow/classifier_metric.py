# -*- coding:utf-8 -*-

# Copyright (C) 2020. Huawei Technologies Co., Ltd. All rights reserved.
# This program is free software; you can redistribute it and/or modify
# it under the terms of the MIT License.
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# MIT License for more details.

"""Metric of classifier task."""
import tensorflow as tf
from zeus.metrics.tensorflow.metrics import MetricBase
from zeus.common import ClassFactory, ClassType


@ClassFactory.register(ClassType.METRIC)
class accuracy(MetricBase):
    """Calculate classification accuracy between output and target."""

    __metric_name__ = 'accuracy'

    def __init__(self, topk=(1, 5)):
        """Init accuracy metric."""
        self.topk = topk

    def __call__(self, output, target, *args, **kwargs):
        """Forward and calculate accuracy."""
        top_accuracy = {}
        is_one = True if len(self.topk) == 1 else False
        if len(output.shape) == 3:
            output = output[0]
        top_1 = -1
        for k in self.topk:
            key = self.__metric_name__ if is_one else 'accuracy_top{}'.format(k)
            in_top_k = tf.cast(tf.nn.in_top_k(output, target, k), tf.float32)
            top_k_accuracy = tf.compat.v1.metrics.mean(in_top_k)
            if top_1 == -1:
                top_1 = top_k_accuracy
                top_accuracy["accuracy"] = top_1
            top_accuracy[key] = top_k_accuracy
        return top_accuracy
