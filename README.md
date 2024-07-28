# Gemini PDFベースチャットボット

## 概要

このプロジェクトは、Google の Gemini AI モデルを使用して、アップロードされた PDF およびマークダウンファイルの内容に基づいて質問に答えるチャットボットアプリケーションです。Streamlit を使用して構築されており、ユーザーフレンドリーなウェブインターフェースを提供します。

## 主な機能

- PDF および Markdown ファイルのアップロードと処理
- アップロードされたファイルの選択的な参照（チェックボックス機能）
- Google Gemini AI モデルを使用した質問応答
- リアルタイムのストリーミング応答
- カスタマイズ可能なシステムプロンプト

## 必要条件

- Python 3.7 以上
- Streamlit
- PyPDF2
- google-generativeai
- markdown

## セットアップ

1. リポジトリをクローンまたはダウンロードします。

2. 必要なライブラリをインストールします：

   ```
   pip install streamlit PyPDF2 google-generativeai markdown
   ```

3. Google AI Studio から Gemini API キーを取得します。

## 使用方法

1. 以下のコマンドでアプリケーションを起動します：

   ```
   streamlit run app.py
   ```

2. ウェブブラウザで表示されるインターフェースに従って操作します：
   - Google API キーを入力します。
   - 使用する Gemini モデルを選択します。
   - PDF または Markdown ファイルをアップロードします。
   - システムプロンプトをカスタマイズします（オプション）。
   - チャットボックスに質問を入力し、AI からの応答を待ちます。

## 注意事項

- アップロードされたファイルの内容は、セッション中のみメモリに保存されます。
- 大きなファイルや多数のファイルをアップロードすると、処理に時間がかかる場合があります。
- API 使用量に応じて料金が発生する可能性があります。Google の料金ポリシーを確認してください。

## ライセンス

このプロジェクトは [MIT ライセンス](https://opensource.org/licenses/MIT) の下で公開されています。

## 貢献

バグ報告や機能リクエストは GitHub の Issues で受け付けています。プルリクエストも歓迎します。

## 免責事項

このアプリケーションは、アップロードされたドキュメントの内容に基づいて回答を生成します。生成された情報の正確性や適切性については、ユーザーご自身で確認してください。