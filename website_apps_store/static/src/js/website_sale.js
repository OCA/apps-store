/**
 *    Copyright 2018 BizzAppDev
 *    License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
 **/
/** @odoo-module **/

import "web.dom_ready";
import publicWidget from "@web/legacy/js/public/public_widget";
import {_t} from "@web/core/l10n/translation";
import {ReCaptcha} from "google_recaptcha.ReCaptchaV3";

const WebsiteSale = publicWidget.registry.WebsiteSale;

WebsiteSale.include({
    // use legacy widget 'events' in Odoo 18
    events: Object.assign({}, WebsiteSale.prototype.events, {
        "click #download_zip": "_onClickDownload",
    }),

    init: function () {
        this._super.apply(this, arguments);
        this._recaptcha = new ReCaptcha();
        this.__started = new Promise((resolve) => (this.__startResolve = resolve));
    },

    willStart: function () {
        const res = this._super(...arguments);
        this._recaptchaLoaded = true;
        this._recaptcha.loadLibs();
        return res;
    },

    _onChangeCombination: function (ev, $parent, combination) {
        this._super.apply(this, arguments);
        if ("is_odoo_module" in combination && combination.is_odoo_module) {
            // fixed selector to match template class 'tech_detail'
            const $tech_detail = this.$(".tech_detail");
            const $license_detail = this.$(".license_detail");
            const $license_url = this.$(".license_url");
            const $author_detail = this.$(".author_detail");
            const $website_detail = this.$(".website_detail");
            const $website_detail_href = this.$("#website_detail_href");
            const $repo_detail = this.$(".repo_detail");
            const $rst_html = this.$(".desc_rst");
            const $app_summary = this.$(".app_summary");
            const $name_product = this.$(".name_product");

            $tech_detail.text(combination.technical_name);
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

    _onClickDownload: async function (ev) {
        ev.preventDefault();
        // Prevent users from crazy clicking
        this.$("#download_zip").addClass("disabled").attr("disabled", "disabled");

        let recaptcha_token_response = "";
        if (this._recaptchaLoaded) {
            const tokenObj = await this._recaptcha.getToken("download_product_zip");
            if (tokenObj.token) {
                recaptcha_token_response = tokenObj.token;
            } else if (tokenObj.error) {
                this.displayNotification({
                    type: "danger",
                    title: _t("Error"),
                    message: tokenObj.error,
                    sticky: true,
                });
                return false;
            }
        }
        const product_template_id = this.$(".product_template_id").val();
        const product_id = this.$(".product_id").val();
        if (product_id) {
            window.location.href =
                "/shop/download_product_zip/" +
                product_template_id +
                "/" +
                product_id +
                "/" +
                recaptcha_token_response;
        } else {
            window.location.href =
                "/shop/download_product_zip/" +
                product_template_id +
                "/" +
                recaptcha_token_response;
        }
    },
});
