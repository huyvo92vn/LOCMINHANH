/* ==========================================================================
   LỘC MINH ANH – script.js (JavaScript thuần, không phụ thuộc thư viện)
   ========================================================================== */

/* >>> ĐIỀN THÔNG TIN THẬT TẠI ĐÂY – tự cập nhật mọi nơi có data-lma trên site <<<
   Để trống = giữ nguyên nhãn "[cập nhật]" và nút gọi nhanh dẫn về trang Liên hệ. */
const LMA = {
  hotline: "0905677429",    // số điện thoại đăng trên hồ sơ thuế (cần chủ doanh nghiệp xác nhận trước khi dùng làm hotline)
  hotlineText: "0905 677 429",
  zalo: "0905677429",
  email: "info@locminhanh.com", // email liên hệ do chủ dự án cung cấp
  address: "11 Thanh Lương 19, phường Hòa Xuân, thành phố Đà Nẵng, Việt Nam", // địa chỉ đăng ký thuế; chưa xác nhận là văn phòng tiếp khách
  hours: "Hỗ trợ 24/7",
  facebook: "https://www.facebook.com/nguyen.khanh.71",
  mapEmbed: "",         // để trống: trang Liên hệ dùng iframe Google Maps dựng sẵn
  formEndpoint: "https://formsubmit.co/ajax/quockhanh2204@gmail.com", // FormSubmit: hộp thư nhận chính
  formCc: "info@locminhanh.com",        // nhận thêm một bản sao tới hộp thư công ty
  formFallback: "https://formsubmit.co/quockhanh2204@gmail.com"       // action dự phòng khi JavaScript không chạy
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
      if (count) count.textContent = n + " loại hình";
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
    form.noValidate = true;
    // Tự bật chế độ gửi nếu trang có endpoint nhưng bản script.js đang chạy bị cũ.
    LMA.formEndpoint = LMA.formEndpoint || "https://formsubmit.co/ajax/quockhanh2204@gmail.com";
    // Số điện thoại Việt Nam: di động 03/05/07/08/09 (10 số) hoặc cố định 02x (11 số), cho phép +84
    const phoneRe = /^(?:\+84|0)(?:(?:3|5|7|8|9)\d{8}|2\d{9})$/;
    const rules = {
      "Họ và tên": (v) => (v.trim().length >= 2 ? "" : "Vui lòng nhập họ và tên."),
      "Số điện thoại": (v) => (phoneRe.test(v.replace(/[\s.\-()]/g, "")) ? "" : "Số điện thoại chưa đúng. Ví dụ: 0905 123 456."),
      Email: (v) => (v === "" || /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v.trim()) ? "" : "Email chưa đúng định dạng."),
      "Loại công trình": (v) => (v ? "" : "Vui lòng chọn loại công trình."),
      "Diện tích (m²)": (v) => (v === "" || (Number(v) > 0 && Number(v) < 1000000) ? "" : "Diện tích phải là số lớn hơn 0."),
      consent: (_v, el) => (el.checked ? "" : "Vui lòng đồng ý để chúng tôi liên hệ lại.")
    };
    const errId = { "Họ và tên": "e-name", "Số điện thoại": "e-phone", Email: "e-email", "Loại công trình": "e-type", "Diện tích (m²)": "e-area", consent: "e-consent" };
    const check = (el) => {
      const rule = rules[el.name]; if (!rule) return true;
      const m = rule(el.value, el), out = $("#" + errId[el.name]);
      el.setAttribute("aria-invalid", m ? "true" : "false");
      if (out) out.textContent = m;
      return !m;
    };
    $$("input,select,textarea", form).forEach((el) => el.addEventListener("blur", () => check(el)));
    const show = (cls, text) => { msg.className = "msg " + cls; msg.textContent = text; msg.hidden = false; msg.focus(); };

    // Quay lại từ trang cảm ơn của FormSubmit (?sent=1)
    if (/[?&]sent=1/.test(location.search)) {
      show("ok", "Cảm ơn bạn. Lộc Minh Anh đã nhận được yêu cầu và sẽ liên hệ lại trong giờ làm việc.");
      history.replaceState(null, "", location.pathname + "#bao-gia");
    }

    // Gửi bằng AJAX để báo đúng kết quả ngay trên trang (không rời trang, không báo cảm ơn giả).
    form.addEventListener("submit", async (e) => {
      e.preventDefault();
      msg.hidden = true;
      const fields = $$("input,select,textarea", form).filter((el) => rules[el.name]);
      const results = fields.map(check);
      const firstBad = fields[results.indexOf(false)];
      if (firstBad) { firstBad.focus(); return; }
      if (form.elements._honey && form.elements._honey.value) return; // bẫy spam (honeypot)
      const submit = $("button[type=submit]", form);
      const label = submit.textContent;
      const fail = "Chưa gửi được yêu cầu. Vui lòng thử lại, hoặc gọi 0905 677 429 / nhắn Zalo để được hỗ trợ ngay.";
      submit.disabled = true; submit.textContent = "Đang gửi…";
      const payload = new FormData(form);
      payload.delete("consent");
      payload.append("_cc", LMA.formCc || "");
      payload.append("Đồng ý liên hệ", "Có");
      payload.append("Nguồn", "Biểu mẫu liên hệ website");
      let sent = false, activation = false;
      try {
        const res = await fetch(LMA.formEndpoint, { method: "POST", body: payload, headers: { Accept: "application/json" } });
        const data = await res.json().catch(() => null);
        if (data && String(data.success) === "true") sent = true;
        else if (data && /activation/i.test(data.message || "")) activation = true;
      } catch (err) { console.warn("[LMA] Lỗi mạng khi gửi yêu cầu.", err); }
      submit.disabled = false; submit.textContent = label;
      if (sent) {
        form.reset();
        show("ok", "Cảm ơn bạn. Lộc Minh Anh đã nhận được yêu cầu và sẽ liên hệ lại ngay.");
        return;
      }
      if (activation) {
        // Dịch vụ nhận yêu cầu chưa được kích hoạt: gửi hộp thư bằng email để không mất yêu cầu của khách.
        const subj = "Yêu cầu tư vấn (" + (form.elements["Họ và tên"].value || "từ website") + ")";
        const body = $$("input,select,textarea", form).filter((el) => rules[el.name] && el.name !== "consent")
          .map((el) => el.name + ": " + (el.checked ? "Có" : el.value)).join("\n");
        location.href = "mailto:" + LMA.email + "?subject=" + encodeURIComponent(subj) + "&body=" + encodeURIComponent(body);
        show("info", "Hệ thống gửi tự động đang tạm gián đoạn. Vui lòng gọi 0905 677 429 hoặc gửi email tới " + LMA.email + ".");
        return;
      }
      show("bad", fail);
    });
  }
})();
