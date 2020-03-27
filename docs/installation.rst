pre-request 安装
====================

本部分文档将向您介绍如何安装pre-request框架到您的环境中

PIP安装
--------

pre-request 目前支持PyPi安装方式，您仅需使用pip命令即可安装成功

.. code-block::

   pip install pre-request


源码安装
--------

如果您希望体验最新版本特性，您可以从github下载最新分支代码到您的本地直接安装

.. code-block::

   python setup.py install

如果您希望在本地以开发模式安装则可以使用以下命令

.. code-block::

   python setup.py develop


本地whl包
----------

当然您也可以在本地构建 whl 进行分发，我们提供了脚本供您一键构建，构建完成后 `dist` 文件夹下可以找到打包后的 whl 文件

.. code-block::

    sh build.sh

