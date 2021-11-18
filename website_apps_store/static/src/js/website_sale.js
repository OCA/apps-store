/* global grecaptcha */
/**
 *    Copyright 2018 BizzAppDev
 *    License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
 **/

odoo.define("website_apps_store.website_sale", function(require) {
    "use strict";

    require("web.dom_ready");
    const ajax = require("web.ajax");
    const sAnimations = require("website.content.snippets.animation");
    const WebsiteSale = sAnimations.registry.WebsiteSale;

    WebsiteSale.include({
        read_events: _.extend({}, WebsiteSale.prototype.read_events, {
            "click #download_zip": "_onClickDownload",
        }),

        init: function() {
            this._super.apply(this, arguments);
            const $captchas = $(".o_website_form_recaptcha");
            ajax.post("/website/recaptcha/", {}).then(result => {
                const data = JSON.parse(result);
                $captchas.append(
                    $(`<div class="g-recaptcha" data-sitekey="${data.site_key}"></div>`)
                );
                if ($captchas.length) {
                    $.getScript("https://www.google.com/recaptcha/api.js");
                }
            });
        },

        _onChangeCombination: function(ev, $parent, combination) {
            this._super.apply(this, arguments);
            if ("is_odoo_module" in combination && combination.is_odoo_module) {
                const $tech_deatil = this.$(".tech_deatil");
                const $license_detail = this.$(".license_detail");
                const $license_url = this.$(".license_url");
                const $author_detail = this.$(".author_detail");
                const $website_detail = this.$(".website_detail");
                const $website_detail_href = this.$("#website_detail_href");
                const $repo_detail = this.$(".repo_detail");
                const $rst_html = this.$(".desc_rst");
                const $app_summary = this.$(".app_summary");
                const $name_product = this.$(".name_product");

                $tech_deatil.text(combination.technical_name);
                $license_detail.text(combination.license);
                $license_url.attr("href", combination.license_url);
                $author_detail.text(combination.author);
                $website_detail.text(combination.website);
                $website_detail_href.attr("href", combination.website);
                $repo_detail.text(combination.repository);
                if ($repo_detail.length) {
                    $repo_detail.parent()[0].href = combination.repository;
                }
                $rst_html.html(combination.rst_html);
                $app_summary.text(combination.app_summary);
                $name_product.text(combination.name_product);
            }
        },

        _onClickDownload: function(ev) {
            ev.preventDefault();
            const google_captcha = $("#g-recaptcha-response").val();
            if (!google_captcha) {
                return;
            }
            if (typeof grecaptcha !== "undefined") {
                grecaptcha.reset();
            }
            const $product_template_id = this.$(".product_template_id");
            const product_template_id = $product_template_id.val();
            const $product_id = this.$(".product_id");
            const product_id = $product_id.val();
            if (product_id) {
                window.location.href =
                    "/shop/download_product_zip/" +
                    product_template_id +
                    "/" +
                    product_id +
                    "/" +
                    google_captcha;
            } else {
                window.location.href =
                    "/shop/download_product_zip/" +
                    product_template_id +
                    "/" +
                    google_captcha;
            }
        },
    });
});
