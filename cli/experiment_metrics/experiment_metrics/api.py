#
# INTEL CONFIDENTIAL
# Copyright (c) 2018 Intel Corporation
#
# The source code contained or described herein and all documents related to
# the source code ("Material") are owned by Intel Corporation or its suppliers
# or licensors. Title to the Material remains with Intel Corporation or its
# suppliers and licensors. The Material contains trade secrets and proprietary
# and confidential information of Intel or its suppliers and licensors. The
# Material is protected by worldwide copyright and trade secret laws and treaty
# provisions. No part of the Material may be used, copied, reproduced, modified,
# published, uploaded, posted, transmitted, distributed, or disclosed in any way
# without Intel's prior express written permission.
#
# No license under any patent, copyright, trade secret or other intellectual
# property right is granted to or conferred upon you by disclosure or delivery
# of the Materials, either expressly, by implication, inducement, estoppel or
# otherwise. Any license under such intellectual property rights must be express
# and approved by Intel in writing.
#

from http import HTTPStatus
import logging
import os

from kubernetes import config, client
from kubernetes.client.rest import ApiException


API_GROUP_NAME = 'aggregator.aipg.intel.com'
RUN_PLURAL = 'runs'
RUN_VERSION = 'v1'

MAX_RETRIES_COUNT = 3

ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
logger = logging.getLogger('metrics')
logger.setLevel(logging.INFO)
logger.addHandler(ch)

run_k8s_name = os.getenv('RUN_NAME')

if run_k8s_name:
    config.load_incluster_config()
    api = client.CustomObjectsApi(client.ApiClient())


def publish(metrics):
    """
    Update metrics in specific Run object
    :param metrics Dict[str,str] of a data to apply
    :return: in case of any problems during update it throws an exception
    """
    if not run_k8s_name:
        logger.info('[no-persist mode] Metrics: {}'.format(metrics))
        return

    with open('/var/run/secrets/kubernetes.io/serviceaccount/namespace', 'r') as ns_file:
        namespace = ns_file.read()

    body = {
        "spec": {
            "metrics": metrics
        }
    }

    for i in range(MAX_RETRIES_COUNT):
        try:
            api.patch_namespaced_custom_object(group='aggregator.aipg.intel.com', namespace=namespace, body=body,
                                               plural=RUN_PLURAL, version=RUN_VERSION, name=run_k8s_name)
            break
        except ApiException as e:
            if e.status != HTTPStatus.CONFLICT or i == MAX_RETRIES_COUNT-1:
                logger.exception("Exception during saving metrics. All {} retries failed!".format(MAX_RETRIES_COUNT), e)
                raise e
