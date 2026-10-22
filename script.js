/* ==========================================================================
   LỘC MINH ANH – script.js (JavaScript thuần, không phụ thuộc thư viện)
   ========================================================================== */

/* >>> ĐIỀN THÔNG TIN THẬT TẠI ĐÂY – tự cập nhật mọi nơi có data-lma trên site <<<
   Để trống = giữ nguyên nhãn "[cập nhật]" và nút gọi nhanh dẫn về trang Liên hệ. */
const LMA = {
  hotline: "",          // ví dụ: "0905123456" (chỉ số, dùng cho tel:)
  hotlineText: "",      // ví dụ: "0905 123 456" (hiển thị)
  zalo: "",             // số Zalo, ví dụ: "0905123456"
  email: "info@locminhanh.com", // email liên hệ do chủ dự án cung cấp
  address: "",          // địa chỉ văn phòng
  hours: "",            // ví dụ: "Thứ 2 – Thứ 7: 7:30 – 17:30"
  facebook: "",         // ví dụ: "https://facebook.com/ten-trang"
  mapEmbed: "",         // URL iframe từ Google Maps > Chia sẻ > Nhúng bản đồ (chỉ phần src)
  formEndpoint: ""      // Nếu có dịch vụ nhận form đã kiểm thử, điền URL HTTPS (xem README)
};

(function () {
  "use strict";
  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => Array.from(r.querySelectorAll(s));

  /* ---- 1. Điền thông tin liên hệ từ LMA ---- */
  const setters = {
    hotline: (el) => { if (LMA.hotline) { el.href = "tel:" + LMA.hotline.replace(/\s/g, ""); if (el.dataset.text !== "no") el.textContent = LMA.hotlineText || LMA.hotline; } },
    zalo: (el) => { if (LMA.zalo) { el.href = "https://zalo.me/" + LMA.zalo.replace(/\D/g, ""); el.target = "_blank"; el.rel = "noopener"; } },
    email: (el) => { if (LMA.email) { el.href = "mailto:" + LMA.email; el.textContent = LMA.email; } },
    address: (el) => { if (LMA.address) el.textContent = LMA.address; },
    hours: (el) => { if (LMA.hours) el.textContent = LMA.hours; },
    facebook: (el) => { if (LMA.facebook) { el.href = LMA.facebook; el.target = "_blank"; el.rel = "noopener noreferrer"; } }
  };
  $$("[data-lma]").forEach((el) => { const f = setters[el.dataset.lma]; if (f) f(el); });

  /* ---- 2. Menu di động ---- */
  const btn = $(".menu-btn"), nav = $("#nav");
  if (btn && nav) {
    const toggle = (open) => {
      nav.classList.toggle("open", open);
      btn.setAttribute("aria-expanded", String(open));
      btn.setAttribute("aria-label", open ? "Đóng menu" : "Mở menu");
    };
    btn.addEventListener("click", () => toggle(!nav.classList.contains("open")));
    document.addEventListener("keydown", (e) => {
      if (e.key === "Escape" && nav.classList.contains("open")) { toggle(false); btn.focus(); }
    });
    nav.addEventListener("click", (e) => { if (e.target.closest("a")) toggle(false); });
  }

  /* ---- 3. Hiện dần khi cuộn (tôn trọng prefers-reduced-motion) ---- */
  const reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  const rv = $$(".rv");
  if (reduce || !("IntersectionObserver" in window)) rv.forEach((e) => e.classList.add("in"));
  else {
    const io = new IntersectionObserver((es) => es.forEach((e) => { if (e.isIntersecting) { e.target.classList.add("in"); io.unobserve(e.target); } }), { threshold: 0.12 });
    rv.forEach((e) => io.observe(e));
  }

  /* ---- 4. Bộ lọc dự án ---- */
  const fbox = $(".filters");
  if (fbox) {
    const cards = $$("[data-cat]");
    const count = $("#fcount");
    const apply = (cat) => {
      let n = 0;
      cards.forEach((c) => { const show = cat === "all" || c.dataset.cat === cat; c.hidden = !show; if (show) n++; });
      $$("button", fbox).forEach((b) => b.setAttribute("aria-pressed", String(b.dataset.filter === cat)));
      if (count) count.textContent = n + " dự án";
    };
    fbox.addEventListener("click", (e) => { const b = e.target.closest("button[data-filter]"); if (b) apply(b.dataset.filter); });
    const h = location.hash.replace("#", "");
    apply(["nha-o", "thuong-mai", "cong-nghiep", "cai-tao"].includes(h) ? h : "all");
  }

  /* ---- 5. Xem ảnh phóng to (lightbox bằng <dialog>) ---- */
  const lb = $("#lb");
  const thumbs = $$("[data-lb]");
  if (lb && thumbs.length && typeof lb.showModal === "function") {
    const img = $("img", lb), cap = $("figcaption", lb);
    let i = 0;
    const show = (n) => { i = (n + thumbs.length) % thumbs.length; const t = thumbs[i]; img.src = t.dataset.lb; img.alt = t.dataset.alt || ""; cap.textContent = t.dataset.alt || ""; };
    thumbs.forEach((t, n) => t.addEventListener("click", () => { show(n); lb.showModal(); }));
    $(".x", lb).addEventListener("click", () => lb.close());
    $(".pv", lb).addEventListener("click", () => show(i - 1));
    $(".nx", lb).addEventListener("click", () => show(i + 1));
    lb.addEventListener("click", (e) => { if (e.target === lb) lb.close(); });
    lb.addEventListener("keydown", (e) => { if (e.key === "ArrowLeft") show(i - 1); if (e.key === "ArrowRight") show(i + 1); });
  }

  /* ---- 6. Bản đồ nhúng ---- */
  const map = $("#map");
  if (map && LMA.mapEmbed) {
    try {
      const url = new URL(LMA.mapEmbed);
      if (url.protocol === "https:" && ["www.google.com", "maps.google.com"].includes(url.hostname) && url.pathname.includes("/maps/embed")) {
        const frame = document.createElement("iframe");
        frame.title = "Bản đồ văn phòng Lộc Minh Anh";
        frame.loading = "lazy";
        frame.referrerPolicy = "no-referrer-when-downgrade";
        frame.src = url.href;
        map.replaceChildren(frame);
      }
    } catch (_) { /* Keep the map placeholder until a valid embed URL is supplied. */ }
  }

  /* ---- 7. Form báo giá: kiểm tra dữ liệu + gửi ---- */
  const form = $("#quote-form");
  if (form) {
    const msg = $("#form-msg");
    // Số điện thoại Việt Nam: di động 03/05/07/08/09 (10 số) hoặc cố định 02x (11 số), cho phép +84
    const phoneRe = /^(?:\+84|0)(?:(?:3|5|7|8|9)\d{8}|2\d{9})$/;
    const rules = {
      name: (v) => (v.trim().length >= 2 ? "" : "Vui lòng nhập họ và tên."),
      phone: (v) => (phoneRe.test(v.replace(/[\s.\-()]/g, "")) ? "" : "Số điện thoại chưa đúng. Ví dụ: 0905 123 456."),
      type: (v) => (v ? "" : "Vui lòng chọn loại công trình."),
      area: (v) => (v === "" || (Number(v) > 0 && Number(v) < 1000000) ? "" : "Diện tích phải là số lớn hơn 0."),
      consent: (_v, el) => (el.checked ? "" : "Vui lòng đồng ý để chúng tôi liên hệ lại.")
    };
    const check = (el) => {
      const rule = rules[el.name]; if (!rule) return true;
      const m = rule(el.value, el), out = $("#e-" + el.name);
      el.setAttribute("aria-invalid", m ? "true" : "false");
      if (out) out.textContent = m;
      return !m;
    };
    $$("input,select,textarea", form).forEach((el) => el.addEventListener("blur", () => check(el)));
    form.addEventListener("submit", async (e) => {
      e.preventDefault();
      msg.hidden = true;
      const fields = $$("input,select,textarea", form).filter((el) => rules[el.name]);
      const results = fields.map(check);
      const firstBad = fields[results.indexOf(false)];
      if (firstBad) { firstBad.focus(); return; }
      if (form.elements.website && form.elements.website.value) return; // bẫy spam (honeypot)
      const show = (cls, text) => { msg.className = "msg " + cls; msg.textContent = text; msg.hidden = false; msg.focus(); };
      if (!LMA.formEndpoint) {
        console.warn("[LMA] Chưa cấu hình LMA.formEndpoint trong script.js – dữ liệu chưa được gửi đi.");
        show("info", "Dữ liệu chưa được gửi: biểu mẫu đang chờ cấu hình dịch vụ nhận. Vui lòng gửi yêu cầu qua email info@locminhanh.com.");
        return;
      }
      const submit = $("button[type=submit]", form); submit.disabled = true;
      try {
        const res = await fetch(LMA.formEndpoint, { method: "POST", body: new FormData(form), headers: { Accept: "application/json" } });
        if (!res.ok) throw new Error(res.status);
        form.reset();
        show("ok", "Cảm ơn bạn. Lộc Minh Anh đã nhận được thông tin và sẽ liên hệ lại sớm nhất trong giờ làm việc.");
      } catch (err) {
        show("bad", "Chưa gửi được biểu mẫu. Vui lòng thử lại hoặc gọi trực tiếp hotline của chúng tôi.");
      } finally { submit.disabled = false; }
    });
  }
})();
