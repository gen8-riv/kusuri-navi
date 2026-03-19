import json
from pathlib import Path


ROOT_PATH = Path(__file__).resolve().parents[1]
HTML_PATH = ROOT_PATH / "index.html"
OLD_HTML_PATH = ROOT_PATH / "kusuri-navi.html"
MANIFEST_PATH = ROOT_PATH / "manifest.json"
SW_PATH = ROOT_PATH / "sw.js"
ICON_192_PATH = ROOT_PATH / "icons" / "icon-192.png"
ICON_512_PATH = ROOT_PATH / "icons" / "icon-512.png"
TEMPLATE_PATH = Path(__file__).resolve().parents[1] / "tasks" / "pharmacist_review_sheet_template.csv"


def main() -> None:
    text = HTML_PATH.read_text(encoding="utf-8")
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    checks = {
        "html_renamed_to_index": HTML_PATH.exists() and not OLD_HTML_PATH.exists(),
        "app_title_updated": "<title>おくすり味ナビ</title>" in text and "<h1>おくすり味ナビ</h1>" in text,
        "header_var_defined": "--header-height:" in text and "--compat-head-height:" in text and "--compat-cat-width:" in text,
        "list_sticky_var_defined": "--list-sticky-height:" in text,
        "teal_palette_applied": "--primary: #2f8fa3;" in text and "--header-start: #67c8d7;" in text,
        "old_purple_removed": "#7c5cbf" not in text and "#a78bda" not in text,
        "viewport_scalable_enabled": 'user-scalable=no' not in text,
        "pwa_meta_tags_present": '<meta name="application-name" content="おくすり味ナビ">' in text and '<meta name="theme-color" content="#2f8fa3">' in text and '<meta name="apple-mobile-web-app-capable" content="yes">' in text and '<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">' in text and '<meta name="apple-mobile-web-app-title" content="おくすり味ナビ">' in text and '<link rel="apple-touch-icon" href="/icons/icon-192.png">' in text and '<link rel="manifest" href="/manifest.json">' in text,
        "manifest_present": MANIFEST_PATH.exists() and manifest["name"] == "おくすり味ナビ" and manifest["short_name"] == "おくすり味ナビ" and manifest["start_url"] == "/" and manifest["display"] == "standalone" and manifest["theme_color"] == "#2f8fa3",
        "service_worker_present": SW_PATH.exists() and 'var CACHE_NAME = "kusuri-navi-v' in SW_PATH.read_text(encoding="utf-8") and 'self.addEventListener("fetch"' in SW_PATH.read_text(encoding="utf-8"),
        "service_worker_registration_present": 'if ("serviceWorker" in navigator)' in text and 'navigator.serviceWorker.register("/sw.js")' in text,
        "runtime_title_normalized": 'if (document.title !== "おくすり味ナビ") {' in text and 'document.title = "おくすり味ナビ";' in text,
        "icon_placeholders_present": ICON_192_PATH.exists() and ICON_512_PATH.exists(),
        "table_hint_present": 'class="table-hint"' in text,
        "bottom_nav_raised_for_ios": ".bottom-nav {" in text and "bottom: 10px; left: 12px; right: 12px;" in text and "padding: 8px 0 calc(env(safe-area-inset-bottom, 8px) + 10px);" in text and "border-radius: 18px;" in text,
        "table_header_visual_boost": "box-shadow: inset 0 -1px 0 rgba(255,255,255,0.16), 0 2px 0 rgba(35,110,128,0.12);" in text and '.compat-sticky-head {' in text and 'top: var(--header-height);' in text,
        "render_card_split": "function renderTasteSection(med)" in text and "function renderMixSection(med)" in text,
        "card_summary_present": "function renderCompatSummary(med)" in text and "summary-pick" in text and "summary-pick-bad" in text,
        "top_three_reco_with_ng_focus": 'compatEntries.good.slice(0, 3)' in text and 'compatEntries.bad.slice(0, 2)' in text and 'summary-label">飲みやすい<' in text and 'summary-label-bad' in text and '\\u26A0 NG' in text,
        "powder_badge_removed": "type-powder" not in text and 'h += \'<span class="type-badge type-powder">' not in text,
        "heart_favorite_enabled": "function getFavIcon(isActive)" in text and "\\u2665" in text and "\\u2661" in text,
        "single_heart_button_in_card": 'renderDetailSections(med);' in text and 'justify-content:flex-end;margin-bottom:4px' not in text,
        "tsumura_normalized": 'function getMakerLabel(med)' in text and 'ツムラ(' in text and 'return med.maker.indexOf("ツムラ(") === 0 ? "ツムラ" : med.maker;' in text,
        "kampo_number_visible": 'function getKampoNumber(med)' in text and "kampo-code" in text and "ツムラ " in text,
        "out_of_scope_removed": 'id: "tulobuterol_tape"' not in text and 'id: "dexamethasone"' not in text,
        "neuro_category_present": 'neuro: "\\u3051\\u3044\\u308c\\u3093"' in text or 'neuro: "けいれん"' in text,
        "dynamic_tabs_present": 'function renderCategoryTabs()' in text and 'function renderTableFilterTabs()' in text and 'function syncPublicFilters()' in text,
        "data_layers_present": 'function getOfficialMedicines()' in text and 'function getReviewedExtensions()' in text and 'function getInternalCandidates()' in text,
        "target_drugs_added": all(
            marker in text
            for marker in [
                'id: "biothree"',
                'id: "makyokansekito"',
                'id: "kikyoto"',
                'id: "keishikashakuyakudaiohto"',
            ]
        ),
        "search_uses_header_var": ".search-area" in text and "top: var(--header-height);" in text,
        "disclaimer_banner_present": 'id="disclaimerBanner"' in text and 'id="disclaimerClose"' in text and '本アプリは医療行為の代替ではありません。服薬に関する最終判断は必ず医師・薬剤師にご確認ください。' in text and '.disclaimer-banner {' in text and 'position: sticky;' not in text[text.find('.disclaimer-banner {'):text.find('.disclaimer-content {')],
        "table_uses_header_var": text.count("top: var(--header-height);") >= 2,
        "multi_med_summary_ui_present": 'id="tableModeSwitch"' in text and 'data-active-mode="single"' in text and 'data-table-mode="single"' in text and 'data-table-mode="multi"' in text and '📋' in text and '💊' in text and 'id="tableAggregateSummary"' in text and 'currentTableMode = "single"' in text and 'selectedTableMedIds = []' in text and '.table-mode-switch::before {' in text and 'container.dataset.activeMode = currentTableMode;' in text,
        "category_tabs_scoped": 'document.querySelectorAll("#categoryTabs .filter-tab")' in text,
        "sticky_metric_fn": "function updateStickyMetrics()" in text,
        "sticky_metric_on_resize": 'window.addEventListener("resize", updateStickyMetrics);' in text,
        "review_defaults_present": 'var reviewDefaults = {' in text and 'verifiedOn: ""' in text and 'status: "pending"' in text,
        "public_filter_applied": 'var list = getPublicMedicines();' in text and 'var savedMeds = getPublicMedicines().filter' in text,
        "review_notes_present": 'id="publicReviewNote"' in text and 'id="tableReviewNote"' in text and 'id="savedReviewNote"' in text,
        "review_nav_hidden_by_default": 'class="nav-item review-nav"' in text and 'style="display:none;"' in text and 'reviewMode' in text,
        "review_dashboard_present": 'id="page-review"' in text and 'id="reviewSummary"' in text and 'id="reviewGroups"' in text,
        "review_editor_present": 'id="reviewEditor"' in text and 'id="reviewAudit"' in text and 'function renderReviewEditor()' in text,
        "review_csv_export_present": 'function buildReviewSheetCsv()' in text and 'function downloadReviewSheet()' in text and 'pharmacist-review-sheet.csv' in text,
        "template_csv_exists": TEMPLATE_PATH.exists(),
        "official_source_map_present": 'var officialSourceMap = {' in text and 'エリスロシンドライシロップ' in text and 'シングレア細粒' in text,
        "official_columns_applied": 'var officialFoodCols = ["ココア", "プリン", "牛乳", "アイス", "お茶", "ヨーグルト", "りんごジュース", "オレンジ飲料", "乳酸菌飲料", "スポーツ飲料"];' in text,
        "source_badge_present": 'function renderSourceBadge(med)' in text and '公的資料掲載' in text and 'officialSourceMeta' in text,
        "inline_mix_legend_present": 'detail-label detail-label-inline' in text and 'detail-inline-legend' in text and '資料上の相性' in text,
        "review_groups_present": 'function renderReviewGroup(' in text and '公的資料掲載' in text and '内部候補' in text and 'row.layer === "internal"' in text,
        "review_csv_layer_column": '"レイヤー"' in text and 'row.layer' in text,
        "review_workflow_present": 'workflowStatus: "internal_candidate"' in text and 'reviewWorkflowLabels' in text and 'approved: "承認済"' in text,
        "review_published_gate": 'med.review.workflowStatus === "published"' in text,
        "review_audit_log_present": 'var reviewAuditStorageKey = "kusuri_review_audit_v1";' in text and 'function appendReviewAudit(' in text and 'function renderReviewAudit()' in text,
        "review_storage_present": 'var reviewRecordStorageKey = "kusuri_review_records_v1";' in text and 'window.addEventListener("storage"' in text,
        "review_action_controls_present": 'data-action="approved"' in text and 'data-action="published"' in text and 'function handleReviewAction(action)' in text,
        "review_csv_workflow_columns": '"workflowStatus"' in text and '"公開日"' in text and '"version"' in text,
        "subjective_review_fields_present": 'subjectiveTastePrimary' in text and 'subjectiveTasteSecondary' in text and 'subjectiveTasteAftertaste' in text and 'subjectiveFlavorPrimary' in text and 'subjectiveFlavorSecondary' in text and 'subjectiveFlavorDetail' in text and 'subjectiveCompat' in text and 'id="reviewTasteDetail"' in text and 'reviewFlavorPrimary' in text and 'reviewCaution' in text,
        "subjective_review_applied_to_public_data": 'm.tastes = m.review.subjectiveTasteTags.slice();' in text and 'm.mixGood = subjectiveMix.good;' in text and 'm.caution = m.review.subjectiveCaution;' in text,
        "subjective_review_csv_columns": '"主な味"' in text and '"副次的な味"' in text and '"後味"' in text and '"味タグ"' in text and '"味詳細"' in text and '"主な香り"' in text and '"副次的な香り"' in text and '"香りの詳細"' in text and '"香り表示"' in text and '"相性要約"' in text,
        "taste_normalization_ui_present": 'function renderTasteSelect(' in text and 'reviewTastePrimary' in text and 'reviewTasteSecondary' in text and 'reviewTasteAftertaste' in text and 'buildTasteTagsFromNormalizedFields' in text,
        "flavor_normalization_ui_present": 'function renderFlavorSelect(' in text and 'reviewFlavorPrimary' in text and 'reviewFlavorSecondary' in text and 'reviewFlavorDetail' in text and 'buildFlavorLabelFromNormalizedFields' in text,
        "saved_page_present": 'id="page-saved"' in text and 'id="savedList"' in text and 'id="savedReviewNote"' in text and 'id="savedFilterTabs"' in text,
        "footer_unified_present": text.count('最終データ更新: 2025年6月') == 3 and text.count('国立成育医療研究センター 薬剤部「粉薬と服薬補助食品の飲み合わせ」') == 3 and text.count('メーカー・ロットにより異なることがあります') == 3,
        "saved_footer_present": 'id="page-saved"' in text and '<div class="footer-update">最終データ更新: 2025年6月</div>' in text,
        "review_footer_unchanged": '※ `?review=1` または `#review` 付きで開いた時のみ表示される内部確認モードです' in text and 'id="page-review"' in text,
        "memo_storage_present": 'var memoStorageKey = "kusuri_memos_v1";' in text and 'function getMemo(id)' in text and 'function setMemo(id, value)' in text,
        "saved_rendering_present": 'function renderMemoSection(med)' in text and 'function renderSaved()' in text and 'data-memo-id="' in text,
        "saved_summary_present": 'id="savedSummary"' in text and 'saved-summary-chip' in text,
        "popup_from_table_present": 'id="medPopup"' in text and 'function openMedPopup(id)' in text and 'data-med-id="' in text and 'navigateToMed' not in text,
        "popup_favorite_present": 'popup-fav-btn' in text and 'data-fav-id="' in text and "document.querySelectorAll('.fav-btn[data-fav-id=\"" in text,
        "saved_cards_collapsed_with_inline_memo": 'function renderInlineMemoEditor(med)' in text and 'showInlineMemoEditor' in text and 'return renderCard(med, { showInlineMemoEditor: true });' in text,
        "saved_filter_tabs_present": 'data-saved-filter="all"' in text and 'data-saved-filter="favorites"' in text and 'data-saved-filter="memo"' in text,
        "table_save_columns_present": 'class="fav-col">お気に入り<' in text and 'class="memo-col">メモ<' in text and 'table-fav-btn' in text and 'table-memo-textarea' in text,
        "table_memo_column_last": "foodLabels.forEach(function(f) { headHtml += '<th class=\"food-col\">' + f + '</th>'; });\n  headHtml += '<th class=\"memo-col\">メモ</th>'" in text and "compat.forEach(function(c) { bodyHtml += \"<td>\" + symMap[c] + \"</td>\"; });\n      bodyHtml += '<td class=\"memo-cell\"><textarea class=\"memo-textarea table-memo-textarea\"" in text,
        "table_memo_density_tuned": ".compat-table .table-memo-textarea {" in text and "min-height: 38px;" in text and "height: 38px;" in text and "padding: 5px 7px;" in text and "font-size: 11px;" in text,
        "category_fix_present": 'id: "montelukast", name: "キプレス細粒 / シングレア細粒"' in text and 'maker: "杏林製薬 / MSD", type: "powder", category: ["allergy"],' in text and 'id: "pranlukast", name: "オノンドライシロップ"' in text and 'maker: "小野薬品工業", type: "powder", category: ["allergy"],' in text and 'id: "cyproheptadine", name: "ペリアクチン散"' in text and 'maker: "日医工", type: "powder", category: ["allergy"],' in text,
        "multi_med_summary_rules_present": 'function buildAggregateCompatSummary(meds)' in text and 'var hasBad = perMed.some(function(item) { return item.code === "B"; });' in text and 'var allGood = perMed.every(function(item) { return item.code === "G"; });' in text and 'var anyGoodOrOk = perMed.some(function(item) { return item.code === "G" || item.code === "O"; });' in text and 'summary.bad.push({' in text and 'summary.good.push({' in text and 'summary.ok.push({' in text,
        "multi_med_selection_rendered_in_table": 'aggregate-selector' in text and 'aggregate-results-panel' in text and 'aggregate-results-placeholder' in text and 'aggregate-med-chip' in text and 'data-select-chip-id' in text and 'id="clearTableSelectionsBtn"' in text and 'id="toggleMultiTableBtn"' in text and 'data-remove-selected-id' in text and 'data-aggregate-toggle' in text and '.aggregate-item-note.is-collapsed' in text and 'grid-template-columns: repeat(3, minmax(0, 1fr));' in text and 'aggregate-item-name' in text and 'pendingAggregateResultFocus = false;' in text and 'pendingAggregateResultPulse = false;' in text and 'flushAggregateResultFeedback()' in text and 'syncTableDetailVisibility()' in text,
        "saved_nav_uses_star": '<div class="nav-item" data-page="page-saved">' in text and 'M12 17.27L18.18 21' in text,
        "table_sticky_head_wrapper_present": 'id="compatStickyHead"' in text and 'id="tableScrollWrap"' in text and 'function syncCompatStickyHead()' in text and 'function scheduleCompatStickySync()' in text and 'tableScrollWrap.addEventListener("scroll", syncCompatStickyHead);' in text and "document.getElementById(\"compatStickyHead\").innerHTML = '<table class=\"compat-table\">' + headHtml + '</table>';" in text and '--compat-head-height' in text and 'stickyCells[idx].style.width = widthValue;' in text and 'setProperty("--compat-cat-width"' in text and 'stickyHead.scrollLeft = wrap.scrollLeft;' in text,
        "table_left_columns_sticky": '.compat-table .cat-cell {' in text and 'position: sticky;' in text and 'left: var(--compat-cat-width, 28px);' in text and '.compat-table thead th.cat-head {' in text and 'headHtml += \'<th class="cat-head"' in text,
        "count_helper_present": 'function buildPublicCountText(visibleCount, totalCount)' in text and '公開母数 ' in text and '表示 ' in text,
        "table_count_present": 'id="tableCount"' in text and 'document.getElementById("tableCount").textContent = buildPublicCountText(filtered.length, totalPublic)' in text,
        "table_and_list_share_category_filter": 'function filterByPublicCategory(list, filterValue)' in text and 'return filterByPublicCategory(list, currentTableFilter);' in text and 'list = filterByPublicCategory(list, currentFilter);' in text,
        "powder_filter_removed": 'powder: "散剤"' not in text and 'currentFilter === "powder"' not in text and 'currentTableFilter === "powder"' not in text,
        "table_footer_source_present": '国立成育医療研究センター 薬剤部「粉薬と服薬補助食品の飲み合わせ」' in text,
        "search_reset_on_init": 'autocomplete="off"' in text and 'if (initialSearchInput) initialSearchInput.value = "";' in text,
        "disclaimer_close_handler_present": 'disclaimerClose.addEventListener("click"' in text and 'disclaimerBanner.classList.add("hidden")' in text,
        "page_switch_scroll_reset": 'function resetPageScroll(page)' in text and 'window.scrollTo(0, 0);' in text and 'setTimeout(apply, 0);' in text and 'resetPageScroll(page);' in text,
    }

    failed = [name for name, ok in checks.items() if not ok]
    for name, ok in checks.items():
        print(f"{name}: {'OK' if ok else 'NG'}")

    if failed:
        raise SystemExit(f"Regression check failed: {', '.join(failed)}")


if __name__ == "__main__":
    main()
