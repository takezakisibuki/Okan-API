from flask import jsonify

def swag():
    json = {
        "swagger": "2.0",
        "info": {
            "description": "これはおかんAPIの仕様書です。",
            "version": "1.0.0",
            "title": "おかんAPI 仕様書",
            "termsOfService": "http://swagger.io/terms/",
            "contact": {
                "email": "kokoroyamasaki.4869@gmail.com"
            },
            "license": {
                "name": "Apache 2.0",
                "url": "http://www.apache.org/licenses/LICENSE-2.0.html"
            }
        },
        "paths": {
            # ① ユーザ情報を取得するAPI パラメータ：user-id
            "/api/test/okan-api": {
                "post": {
                    "tags": [
                        "test"
                    ],
                    "summary": "【テスト】日記を投稿するAPI",
                    "description": "",
                    "consumes": [
                        "multipart/form-data"
                    ],
                    "produces": [
                        "application/json"
                    ],
                    "parameters": [
                        {
                            "name": "user-id",
                            "in": "formData",
                            "description": "ユーザid",
                            "required": True,
                            "type": "integer",
                            "format": "int64"
                        },
                        {
                            "name": "diary-content",
                            "in": "formData",
                            "description": "日記内容",
                            "required": True,
                            "type": "string"
                        },
                    ],
                    "responses": {
                        "200": {
                            "description": "successful operation",
                            "schema": {
                                "type": "object",
                                "properties": {
                                    "diary-content": {
                                        "type": "string",
                                        "example": "今日はおかんがおかんしてた"
                                    },
                                },
                            }
                        }
                    },
                }
            },
            # ② 日記を取得するAPI
            "/api/test/diary": {
                "get": {
                    "tags": [
                        "test"
                    ],
                    "summary": "【テスト】日記を取得するAPI",
                    "description": "",
                    "consumes": [
                        "multipart/form-data"
                    ],
                    "produces": [
                        "application/json"
                    ],
                    "parameters": [
                        {
                            "name": "diary-id",
                            "in": "query",
                            "description": "日記id",
                            "required": True,
                            "type": "integer",
                        },
                    ],
                    "responses": {
                        "200": {
                            "description": "successful operation",
                            "schema": {
                                "type": "object",
                                "properties": {
                                    'id':{
                                        "type": "integer",
                                        "example": "1"
                                    },
                                    'content':{
                                        "type": "string",
                                        "example": "あんたの日記内容やでぇ"
                                    },
                                    'comment': {
                                        "type": "string",
                                        "example": "おかんからのテストコメントやでぇ"
                                    },
                                    'time': {
                                        "type": "string",
                                        "example": "2023-10-1"
                                    },
                                },
                            }
                        }
                    },
                }
            },
            # ③ 指定月の日記一覧を取得するAPI
            "/api/test/monthly": {
                "get": {
                    "tags": [
                        "test"
                    ],
                    "summary": "【テスト】指定月の日記一覧を取得するAPI",
                    "description": "",
                    "consumes": [
                        "multipart/form-data"
                    ],
                    "produces": [
                        "application/json"
                    ],
                    "parameters": [
                        {
                            "name": "user-id",
                            "in": "query",
                            "description": "ユーザid",
                            "required": True,
                            "type": "integer",
                            "format": "int64"
                        },
                        {
                            "name": "month",
                            "in": "query",
                            "description": "月",
                            "required": True,
                            "type": "integer"
                        },
                    ],
                    "responses": {
                        "200": {
                            "description": "successful operation",
                            "schema": {
                                "type": "object",
                                "properties": {
                                    "diary_list": {
                                        "type": "array",
                                        "example":[{ "id": 1, "date": "2023-10-1" },{ "id": 2, "date": "2023-10-2" }]
                                    },
                                },
                            }
                        }
                    },
                }
            },
            # ④ ギフトガチャを回すAPI
            "/api/test/gift-rand": {
                "post": {
                    "tags": [
                        "test"
                    ],
                    "summary": "【テスト】ギフトガチャを回すAPI",
                    "description": "",
                    "consumes": [
                        "multipart/form-data"
                    ],
                    "produces": [
                        "application/json"
                    ],
                    "parameters": [
                        {
                            "name": "user-id",
                            "in": "formData",
                            "description": "ユーザid",
                            "required": True,
                            "type": "integer",
                            "format": "int64"
                        },
                    ],
                    "responses": {
                        "200": {
                            "description": "successful operation",
                            "schema": {
                                "type": "object",
                                "properties": {
                                    "gift_number": {
                                        "type": "integer",
                                        "example": 20
                                    },
                                },
                            }
                        }
                    },
                }
            },
            # ⑤ ギフトフラグを取得するAPI
            "/api/test/gift-flag": {
                "get": {
                    "tags": [
                        "test"
                    ],
                    "summary": "【テスト】ギフトフラグを取得するAPI",
                    "description": "",
                    "consumes": [
                        "multipart/form-data"
                    ],
                    "produces": [
                        "application/json"
                    ],
                    "parameters": [
                        {
                            "name": "user-id",
                            "in": "query",
                            "description": "ユーザid",
                            "required": True,
                            "type": "integer",
                            "format": "int64"
                        },
                    ],
                    "responses": {
                        "200": {
                            "description": "successful operation",
                            "schema": {
                                "type": "object",
                                "properties": {
                                    "gift_flag": {
                                        "type": "array",
                                        "example": [0 for _ in range(25)]
                                    },
                                },
                            }
                        }
                    },
                }
            },
            "/authorize": {
                "post": {
                    "tags": [
                        "okan-api(WIP) まだ実装してないよ"
                    ],
                    "summary": "API認証用のトークン発行API",
                    "description": "",
                    "consumes": [
                        "multipart/form-data"
                    ],
                    "produces": [
                        "application/json"
                    ],
                    "parameters": [
                        {
                            "name": "id",
                            "in": "query",
                            "description": "ユーザid",
                            "required": True,
                            "type": "integer",
                            "format": "int64"
                        },
                        {
                            "name": "password",
                            "in": "query",
                            "description": "パスワード",
                            "required": True,
                            "type": "string"
                        },
                    ],
                    "responses": {
                        "200": {
                            "description": "successful operation",
                            "schema": {
                                "type": "object",
                                "properties": {
                                    "token": {
                                        "token": "hogehogefugafuga",
                                        "id": "int"
                                    },
                                },
                            }
                        }
                    },
                }
            },
            # ① ユーザ情報を取得するAPI パラメータ：user-id
            "/api/okan-api": {
                "post": {
                    "tags": [
                        "okan-api(WIP) まだ実装してないよ"
                    ],
                    "summary": "日記を投稿するAPI",
                    "description": "",
                    "consumes": [
                        "multipart/form-data"
                    ],
                    "produces": [
                        "application/json"
                    ],
                    "parameters": [
                        {
                            "name": "user-id",
                            "in": "formData",
                            "description": "ユーザid",
                            "required": True,
                            "type": "integer",
                            "format": "int64"
                        },
                        {
                            "name": "diary-content",
                            "in": "formData",
                            "description": "日記内容",
                            "required": True,
                            "type": "string"
                        },
                    ],
                    "responses": {
                        "200": {
                            "description": "successful operation",
                            "schema": {
                                "type": "object",
                                "properties": {
                                    "diary-content": {
                                        "type": "string",
                                        "example": "今日はおかんがおかんしてた"
                                    },
                                },
                            }
                        }
                    },
                }
            },
            # ② 日記を取得するAPI
            "/api/diary": {
                "get": {
                    "tags": [
                        "okan-api(WIP) まだ実装してないよ"
                    ],
                    "summary": "日記を取得するAPI",
                    "description": "",
                    "consumes": [
                        "multipart/form-data"
                    ],
                    "produces": [
                        "application/json"
                    ],
                    "parameters": [
                        {
                            "name": "diary-id",
                            "in": "query",
                            "description": "日記id",
                            "required": True,
                            "type": "integer",
                        },
                    ],
                    "responses": {
                        "200": {
                            "description": "successful operation",
                            "schema": {
                                "type": "object",
                                "properties": {
                                    'id':{
                                        "type": "integer",
                                        "example": "1"
                                    },
                                    'content':{
                                        "type": "string",
                                        "example": "あんたの日記内容やでぇ"
                                    },
                                    'comment': {
                                        "type": "string",
                                        "example": "おかんからのテストコメントやでぇ"
                                    },
                                    'time': {
                                        "type": "string",
                                        "example": "2023-10-1"
                                    },
                                },
                            }
                        }
                    },
                }
            },
            # ③ 指定月の日記一覧を取得するAPI
            "/api/monthly": {
                "get": {
                    "tags": [
                        "okan-api(WIP) まだ実装してないよ"
                    ],
                    "summary": "指定月の日記一覧を取得するAPI",
                    "description": "",
                    "consumes": [
                        "multipart/form-data"
                    ],
                    "produces": [
                        "application/json"
                    ],
                    "parameters": [
                        {
                            "name": "user-id",
                            "in": "query",
                            "description": "ユーザid",
                            "required": True,
                            "type": "integer",
                            "format": "int64"
                        },
                        {
                            "name": "month",
                            "in": "query",
                            "description": "月",
                            "required": True,
                            "type": "integer",
                        },
                         {
                            "name": "year",
                            "in": "query",
                            "description": "年",
                            "required": True,
                            "type": "integer"
                        },
                    ],
                    "responses": {
                        "200": {
                            "description": "successful operation",
                            "schema": {
                                "type": "object",
                                "properties": {
                                    "diary_list": {
                                        "type": "array",
                                        "example":[{ "id": 1, "date": "2023-10-1" },{ "id": 2, "date": "2023-10-2" }]
                                    },
                                },
                            }
                        }
                    },
                }
            },
            # ④ ギフトガチャを回すAPI
            "/api/gift-rand": {
                "post": {
                    "tags": [
                        "okan-api(WIP) まだ実装してないよ"
                    ],
                    "summary": "ギフトガチャを回すAPI",
                    "description": "",
                    "consumes": [
                        "multipart/form-data"
                    ],
                    "produces": [
                        "application/json"
                    ],
                    "parameters": [
                        {
                            "name": "user-id",
                            "in": "formData",
                            "description": "ユーザid",
                            "required": True,
                            "type": "integer",
                            "format": "int64"
                        },
                    ],
                    "responses": {
                        "200": {
                            "description": "successful operation",
                            "schema": {
                                "type": "object",
                                "properties": {
                                    "gift_number": {
                                        "type": "integer",
                                        "example": 20
                                    },
                                },
                            }
                        }
                    },
                }
            },
            # ⑤ ギフトフラグを取得するAPI
            "/api/gift-flag": {
                "get": {
                    "tags": [
                        "okan-api(WIP) まだ実装してないよ"
                    ],
                    "summary": "ギフトフラグを取得するAPI",
                    "description": "",
                    "consumes": [
                        "multipart/form-data"
                    ],
                    "produces": [
                        "application/json"
                    ],
                    "parameters": [
                        {
                            "name": "user-id",
                            "in": "query",
                            "description": "ユーザid",
                            "required": True,
                            "type": "integer",
                            "format": "int64"
                        },
                    ],
                    "responses": {
                        "200": {
                            "description": "successful operation",
                            "schema": {
                                "type": "object",
                                "properties": {
                                    "gift_flag": {
                                        "type": "array",
                                        "example": [0 for _ in range(25)]
                                    },
                                },
                            }
                        }
                    },
                }
            },
            #ユーザを登録しよう
            "/api/registration": {
                "post": {
                    "tags": [
                        "okan-api(WIP) まだ実装してないよ"
                    ],
                    "summary": "ユーザを登録しよう",
                    "description": "",
                    "consumes": [
                        "multipart/form-data"
                    ],
                    "produces": [
                        "application/json"
                    ],
                    "parameters": [
                        {
                            "name": "user-id",
                            "in": "formData",
                            "description": "ユーザid",
                            "required": True,
                            "type": "integer",
                            "format": "int64"
                        },
                        {
                            "name": "password",
                            "in": "formData",
                            "description": "パスワード",
                            "required": True,
                            "type": "string"
                        },
                    ],
                    "responses": {
                        "200": {
                            "description": "successful operation",
                            "schema": {
                                "type": "object",
                                "properties": {
                                    "diary-content": {
                                        "message": "ユーザーが登録されました", 
                                        "user_id": 111
                                    },
                                },
                            }
                        }
                    },
                }
            },
            "/authorize": {
                "post": {
                    "tags": [
                        "okan-api(WIP) まだ実装してないよ"
                    ],
                    "summary": "API認証用のトークン発行API",
                    "description": "",
                    "consumes": [
                        "multipart/form-data"
                    ],
                    "produces": [
                        "application/json"
                    ],
                    "parameters": [
                        {
                            "name": "id",
                            "in": "formData",
                            "description": "ユーザid",
                            "required": True,
                            "type": "integer",
                            "format": "int64"
                        },
                        {
                            "name": "password",
                            "in": "formData",
                            "description": "パスワード",
                            "required": True,
                            "type": "string"
                        },
                    ],
                    "responses": {
                        "200": {
                            "description": "successful operation",
                            "schema": {
                                "type": "object",
                                "properties": {
                                    "token": {
                                        "token": "hogehogefugafuga",
                                        "id": "int"
                                    },
                                },
                            }
                        }
                    },
                }
            },
            "/api/delete_diary": {
                "delete": {
                    "tags": [
                        "okan-api(WIP) まだ実装してないよ"
                    ],
                    "summary": "日記削除のAPI",
                    "description": "",
                    "consumes": [
                        "multipart/form-data"
                    ],
                    "produces": [
                        "application/json"
                    ],
                    "parameters": [
                        {
                            "name": "diary-id",
                            "in": "formData",
                            "description": "削除したい日記のdiary_id",
                            "required": True,
                            "type": "integer",
                            "format": "int64"
                        },
                    ],
                    "responses": {
                        "200": {
                            "description": "successful operation",
                            "schema": {
                                "type": "object",
                                "properties": {
                                    "token": {
                                        "token": "hogehogefugafuga",
                                        "id": "int"
                                    },
                                },
                            }
                        }
                    },
                }
            },
        },
        "externalDocs": {
            "description": "Find out more about Swagger",
            "url": "http://swagger.io"
	    }
    }
    return jsonify(json)