# -*- coding: utf-8 -*-
"""公网 IP 查询页面"""

from ui.widgets import create_label, create_button, BasePage
from tools.ip_lookup import get_public_ip


class IpLookupPage(BasePage):
    def __init__(self, status_callback=None, result_callback=None):
        super().__init__(status_callback, result_callback)

        self.layout.addWidget(create_label("公网 IP 查询"), 0, 0, 1, 5)

        self.btn_query = create_button("查询本机公网 IP")
        self.btn_query.clicked.connect(self._on_query)
        self.layout.addWidget(self.btn_query, 1, 0)

    def _on_query(self):
        self.btn_query.setEnabled(False)
        self.status_callback("正在查询公网 IP...")
        try:
            result = get_public_ip()
            self.result_callback(result)
            self.status_callback("查询完成")
        except Exception as e:
            self.result_callback(f"Error: {e}")
        finally:
            self.btn_query.setEnabled(True)
