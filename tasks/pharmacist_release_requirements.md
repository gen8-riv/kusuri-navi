# Pharmacist Release Requirements

## Mandatory Before Claiming Pharmacist Supervision
- `薬剤師監修` と表示する前に、実在する薬剤師本人が全掲載薬について内容確認を完了していること。
- 監修者名、確認日、確認対象バージョンを記録すること。
- AIが生成した記載をそのまま載せず、監修者が修正可否を判断したログを残すこと。

## High-Risk Fields Requiring Human Review
- 味の表現
- 飲み合わせの良し悪し
- 注意喚起文
- 小児での使い方に関するニュアンス表現

## Safer Release Rule
- 公式資料で確認できる客観項目:
  - 製品名
  - 一般名
  - メーカー名
  - 剤形
  - 基本的な禁忌・注意の存在
- 客観資料で裏取りしにくい主観項目:
  - 味
  - 飲ませやすさ
  - 混ぜ物との相性

## Recommendation
- App Store 提出前に、掲載薬ごとのレビュー表を別ファイルで運用する。
- 監修完了前の薬は公開対象から外す。
- 将来的には各薬に `reviewed_by_pharmacist` と `last_reviewed_at` を持たせる実装へ移行する。
