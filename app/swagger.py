from flask import jsonify

def swag():
    json = {
        "swagger": "2.0",
        "info": {
            "description": "これはおかんAPIの仕様書です。",
            "version": "1.1.0",
            "title": "おかんAPI 仕様書",
            "termsOfService": "http://swagger.io/terms/",
            "contact": {
                "email": "kokoroyamasaki.4869@gmail.com"
            },
        },
        "paths": {
            # A. 認証用のトークン発行API(...なんだけど公開したら後悔するので公開しません。)
            # B. ユーザを登録しよう
            "/api/registration": {
                "post": {
                    "tags": [
                        "認証用API"
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
                                        "type": "string", 
                                        "example": "ユーザーが登録されました"
                                    },
                                    'user_id':{
                                        "type": "integer",
                                        "example": "123"
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
                    "security": [
                        {
                            "Bearer": []
                        }
                    ],
                    "tags": [
                        "おかんAPI"
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
                                    'date': {
                                        "type": "string",
                                        "example": "2023-10-1"
                                    },
                                    'user_id':{
                                        "type": "integer",
                                        "example": "123"
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
                    "security": [
                        {
                            "Bearer": []
                        }
                    ],
                    "tags": [
                        "おかんAPI"
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
                                    'date': {
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
                    "security": [
                        {
                            "Bearer": []
                        }
                    ],
                    "tags": [
                        "おかんAPI"
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
                    "security": [
                        {
                            "Bearer": []
                        }
                    ],
                    "tags": [
                        "おかんAPI"
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
                                    'user_id':{
                                        "type": "integer",
                                        "example": "123"
                                    },
                                    "gift_flag": {
                                        "type": "array",
                                        "example": [0 for _ in range(20)]
                                    },
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
                    "security": [
                        {
                            "Bearer": []
                        }
                    ],
                    "tags": [
                        "おかんAPI"
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
                                    'user_id':{
                                        "type": "integer",
                                        "example": "123"
                                    },
                                    "gift_flag": {
                                        "type": "array",
                                        "example": [0 for _ in range(20)]
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
                        "開発者向けAPI"
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
                                    "message": {
                                        "type": "string",
                                        "example": "日記エントリが正常に削除されました"
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
	    },
        "securityDefinitions": {
            "Bearer": {
                "type": "apiKey",
                "name": "Authorization",
                "in": "header"
            }
        },
        "components": {
            "securitySchemes": {
                "Bearer": {
                    "type": "http",
                    "scheme": "bearer",
                    "bearerFormat": "JWT" 
                }
            }
        },
    }
    return jsonify(json)