# -*- coding: utf-8 -*-
"""
TencentBlueKing is pleased to support the open source community by making 蓝鲸智云-用户管理(Bk-User) available.
Copyright (C) 2017-2021 THL A29 Limited, a Tencent company. All rights reserved.
Licensed under the MIT License (the "License"); you may not use this file except in compliance with the License.
You may obtain a copy of the License at http://opensource.org/licenses/MIT
Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on
an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the
specific language governing permissions and limitations under the License.
"""
# Generated by Django 1.11.23 on 2020-07-29 07:49
from __future__ import unicode_literals

from django.db import migrations


def forwards_func(apps, schema_editor):
    """添加内建字段信息"""
    DynamicFieldInfo = apps.get_model("profiles", "DynamicFieldInfo")

    max_order = max(DynamicFieldInfo.objects.all().values_list("order", flat=True))

    DynamicFieldInfo.objects.create(
        name='account_expiration_date',
        display_name='账号过期时间',
        type='string',
        require=False,
        unique=False,
        editable=True,
        builtin=True,
        order=max_order+1,
        display_name_en='account_expiration_date',
        display_name_zh_hans='账号过期时间',
        visible=True
    )
    DynamicFieldInfo.objects.create(
        name='last_login_time',
        display_name='最近登陆时间',
        type='string',
        require=False,
        unique=False,
        editable=False,
        builtin=True,
        order=max_order+2,
        display_name_en='last_login_time',
        display_name_zh_hans='最近登录时间',
        configurable=False,
        visible=False)
    DynamicFieldInfo.objects.create(
        name='create_time',
        display_name='创建时间',
        type='string',
        require=False,
        unique=False,
        editable=False,
        builtin=True,
        order=max_order+3,
        display_name_en='create_time',
        display_name_zh_hans='创建时间',
        configurable=False,
        visible=True)

    DynamicFieldInfo.objects.filter(name='qq').update(visible=False)
    DynamicFieldInfo.objects.filter(name='wx_userid').update(visible=False)


class Migration(migrations.Migration):

    dependencies = [
        ("profiles", "0024_expirationnoticerecord"),
    ]

    operations = [migrations.RunPython(forwards_func)]
