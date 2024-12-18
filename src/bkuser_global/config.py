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
import environ

def init_patch():
    import pymysql
    import urllib3

    # no more useless warning

    urllib3.disable_warnings()

    # ==============================================================================
    # Patching
    # ==============================================================================
    pymysql.install_as_MySQLdb()
    # Patch version info to forcely pass Django client check
    setattr(pymysql, "version_info", (1, 4, 6, "final", 0))


class DatabaseEngine:
    """数据库引擎"""

    MYSQL = "django.db.backends.mysql"
    OCEANBASE = "cw_cornerstone.db.oceanbase.backend"
    DAMENG = "cw_cornerstone.db.dameng.backend"


    @classmethod
    def get_db_engine(cls, db_type: str) -> str:
        """获取数据库引擎"""
        return getattr(cls, db_type.upper(), cls.DAMENG)


class DatabaseOptions:
    """数据库连接配置"""
    DAMENG_DB = "DAMENG"
    MYSQL_DB = "MYSQL"
    OCEANBASE_DB = "OCEANBASE"
    @classmethod
    def get_db_options(cls, db: str, db_name: str) -> dict:
        """获取数据库引擎"""
        db_options_map = {
            cls.MYSQL_DB: {"charset": "utf8mb4"},
            cls.OCEANBASE_DB: {"charset": "utf8mb4"},
            cls.DAMENG_DB: {"schema": db_name},
        }

        return db_options_map.get(db.upper(), cls.DAMENG_DB)


def get_db_config(env: environ.Env, db_prefix: str) -> dict:
    """通用 DB 配置获取方法"""
    db_type = env("{}_TYPE".format(db_prefix), default=DatabaseOptions.DAMENG_DB)
    return {
        "default": {
            "ENGINE": DatabaseEngine.get_db_engine(db_type),
            "NAME": env(f"{db_prefix}_NAME"),
            "USER": env(f"{db_prefix}_USER"),
            "PASSWORD": env(f"{db_prefix}_PASSWORD"),
            "HOST": env(f"{db_prefix}_HOST"),
            "PORT": env(f"{db_prefix}_PORT"),
            "OPTIONS": DatabaseOptions.get_db_options(db_type, env(f"{db_prefix}_NAME")),
            "TEST": {"CHARSET": "utf8mb4", "COLLATION": "utf8mb4_general_ci"},
        }
    }
