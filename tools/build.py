#!/usr/bin/env python3
"""Sinh toàn bộ các trang HTML tĩnh của website Lộc Minh Anh.
Chạy:  python3 tools/build.py   (từ thư mục gốc của repo)
Không bắt buộc: site đã được sinh sẵn, chỉ chạy lại nếu muốn sửa nội dung/header/footer tại một chỗ."""
import os, json, html
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BASE = "https://huyvo92vn.github.io/LOCMINHANH/"   # đổi khi dùng tên miền riêng
TODAY = "2026-10-19"
SLOGAN = "Vững bền kiến tạo tương lai"
esc = html.escape

# ---------------------------------------------------------------- biểu tượng (SVG nét mảnh)
def svg(d, cls=""):
    return ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" '
            'stroke-linejoin="round" aria-hidden="true" focusable="false"%s>%s</svg>' % (' class="%s"' % cls if cls else "", d))
IC = {
 "phone": svg('<path d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2z"/>'),
 "mail": svg('<rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3 7 9 6 9-6"/>'),
 "pin": svg('<path d="M12 21s7-6.2 7-11a7 7 0 1 0-14 0c0 4.8 7 11 7 11z"/><circle cx="12" cy="10" r="2.5"/>'),
 "clock": svg('<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>'),
 "fb": svg('<path d="M14 8h3V4h-3a4 4 0 0 0-4 4v3H7v4h3v6h4v-6h3l1-4h-4V8z"/>'),
 "layers": svg('<path d="m12 3 9 5-9 5-9-5 9-5z"/><path d="m3 13 9 5 9-5M3 17.5l9 5 9-5" opacity=".6"/>'),
 "build": svg('<path d="M4 21V8l6-4v17M10 21V11l10 3v7M3 21h18M7 11h.01M7 15h.01M14 17h.01M17 17h.01"/>'),
 "brush": svg('<path d="M4 20c3 0 5-1 5-4l-2-2c-3 0-3 3-3 6zM9 14 20 3l1 1-11 11"/>'),
 "wrench": svg('<path d="M14 6a4 4 0 0 0 5 5l-9 9a2.1 2.1 0 0 1-3-3l9-9a4 4 0 0 0-2-2z"/>'),
 "clip": svg('<rect x="6" y="4" width="12" height="17" rx="2"/><path d="M9 4h6v3H9zM9 12h6M9 16h4"/>'),
 "shield": svg('<path d="M12 3 5 6v6c0 4.5 3 7.5 7 9 4-1.5 7-4.5 7-9V6l-7-3z"/><path d="m9 12 2 2 4-4"/>'),
 "eye": svg('<path d="M2 12s4-7 10-7 10 7 10 7-4 7-10 7S2 12 2 12z"/><circle cx="12" cy="12" r="3"/>'),
 "calendar": svg('<rect x="4" y="5" width="16" height="16" rx="2"/><path d="M4 10h16M9 3v4M15 3v4"/>'),
 "helmet": svg('<path d="M4 16a8 8 0 0 1 16 0M2 16h20v2H2zM12 4v5"/>'),
 "handshake": svg('<path d="m3 12 4-4 4 2 4-2 6 6-6 5-4-1-3 2-5-4z"/>'),
 "chat": svg('<path d="M4 5h16v11H9l-5 4z"/><path d="M8 9h8M8 12h5"/>'),
 "doc": svg('<path d="M7 3h7l5 5v13H7z"/><path d="M14 3v5h5M10 13h6M10 17h6"/>'),
 "menu": svg('<path d="M4 7h16M4 12h16M4 17h16"/>'),
 "arrow": svg('<path d="M5 12h14M13 6l6 6-6 6"/>'),
}
ROOF = ('<svg viewBox="0 0 30 16" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" '
        'stroke-linejoin="round" aria-hidden="true"><path d="M2 14 15 3l13 11"/></svg>')
def rule(): return '<div class="rule" aria-hidden="true">%s</div>' % ROOF

# ---------------------------------------------------------------- dữ liệu nội dung
NAV = [("Trang chủ", "index.html"), ("Giới thiệu", "gioi-thieu.html"), ("Dịch vụ", "dich-vu.html"),
       ("Dự án", "du-an.html"), ("Quy trình", "quy-trinh.html"), ("Tin tức", "tin-tuc.html"), ("Liên hệ", "lien-he.html")]

PH = lambda s: '<span class="ph-val">[%s]</span>' % s

SERVICES = [
 dict(id="tong-thau-tron-goi", ic="layers", name="Tổng thầu thiết kế – thi công trọn gói",
  short="Một hợp đồng, một đầu mối chịu trách nhiệm từ thiết kế đến bàn giao.",
  intro="Chủ đầu tư làm việc với một đầu mối duy nhất. Lộc Minh Anh điều phối thiết kế, vật tư, nhân lực và an toàn để công trình đi đúng kế hoạch đã ký.",
  scope=["Khảo sát hiện trạng, đo đạc, tư vấn phương án", "Thiết kế kiến trúc, kết cấu, điện nước", "Lập dự toán chi tiết và hợp đồng trọn gói", "Hỗ trợ thủ tục xin phép xây dựng", "Thi công, giám sát, nghiệm thu từng giai đoạn", "Hoàn công và bàn giao"],
  steps=["Tiếp nhận nhu cầu", "Thiết kế và báo giá", "Ký hợp đồng", "Thi công và giám sát", "Bàn giao, bảo hành"],
  commit=["Dự toán bóc tách theo hạng mục, ghi rõ chủng loại vật tư", "Tiến độ được ghi trong hợp đồng", "Chi phí phát sinh chỉ thực hiện khi chủ đầu tư xác nhận bằng văn bản"]),
 dict(id="xay-dung-dan-dung-cong-nghiep", ic="build", name="Xây dựng dân dụng và công nghiệp",
  short="Nhà ở, văn phòng, cửa hàng, nhà xưởng, kho bãi.",
  intro="Thi công phần thô và hạ tầng kỹ thuật cho công trình dân dụng và công nghiệp, bám sát bản vẽ và tiêu chuẩn kỹ thuật đã được duyệt.",
  scope=["Móng, khung, sàn, mái, tường bao", "Nhà phố, biệt thự, nhà ở gia đình", "Văn phòng, cửa hàng, công trình thương mại", "Nhà xưởng, kho bãi", "Sân, đường nội bộ, hạ tầng kỹ thuật đi kèm"],
  steps=["Nhận bản vẽ, lập biện pháp thi công", "Chuẩn bị mặt bằng, vật tư", "Thi công phần ngầm, phần thân", "Nghiệm thu từng giai đoạn", "Bàn giao phần thô hoặc trọn gói"],
  commit=["Thi công đúng bản vẽ và tiêu chuẩn kỹ thuật được duyệt", "Nghiệm thu cốt thép và đổ bê tông có biên bản trước khi sang bước tiếp", "Nhật ký công trình và ảnh cập nhật định kỳ cho chủ đầu tư"]),
 dict(id="hoan-thien-noi-ngoai-that", ic="brush", name="Hoàn thiện nội ngoại thất",
  short="Từ mặt tiền, sơn, ốp lát đến nội thất theo thiết kế.",
  intro="Giai đoạn quyết định cảm nhận khi sử dụng. Chúng tôi thống nhất mẫu vật liệu và bản vẽ chi tiết trước khi thi công để kết quả đúng như đã duyệt.",
  scope=["Ốp lát, sơn bả, trần thạch cao", "Cửa, lan can, cầu thang", "Mặt tiền, sân vườn, cổng và hàng rào", "Nội thất theo thiết kế: tủ bếp, tủ áo, vách ốp", "Lắp đặt thiết bị vệ sinh, thiết bị điện"],
  steps=["Chốt phong cách và vật liệu", "Duyệt mẫu thực tế", "Thi công hoàn thiện", "Kiểm tra chi tiết", "Bàn giao và xử lý tồn đọng"],
  commit=["Duyệt mẫu vật liệu trước khi thi công", "Hoàn thiện theo bản vẽ chi tiết đã thống nhất", "Biên bản bàn giao ghi rõ hạng mục tồn đọng và thời hạn xử lý"]),
 dict(id="cai-tao-sua-chua", ic="wrench", name="Cải tạo và sửa chữa công trình",
  short="Nâng cấp, mở rộng, chống thấm, gia cố công trình hiện hữu.",
  intro="Mỗi công trình cũ có hiện trạng riêng. Chúng tôi khảo sát kỹ trước khi báo giá để hạn chế phát sinh và giữ an toàn cho khu vực xung quanh.",
  scope=["Cải tạo mặt bằng, nâng tầng, mở rộng", "Chống thấm, chống nứt, gia cố kết cấu", "Thay mới hệ thống điện, nước", "Sơn sửa, thay mới mặt tiền", "Phương án che chắn khi chủ nhà vẫn ở hoặc đang kinh doanh"],
  steps=["Khảo sát hiện trạng", "Đánh giá kết cấu", "Phương án và báo giá", "Thi công cải tạo", "Nghiệm thu, vệ sinh bàn giao"],
  commit=["Khảo sát hiện trạng trước khi báo giá", "Biện pháp che chắn và an toàn cho khu vực lân cận", "Dọn dẹp, vệ sinh khi bàn giao"]),
 dict(id="quan-ly-du-an", ic="clip", name="Quản lý dự án",
  short="Giám sát tiến độ, chất lượng, an toàn lao động tại công trường.",
  intro="Dành cho chủ đầu tư cần một đơn vị kiểm soát tiến độ và chất lượng, kể cả khi dự án có nhiều nhà thầu thực hiện.",
  scope=["Lập kế hoạch tiến độ và kiểm soát chi phí", "Giám sát chất lượng vật tư và thi công", "Quản lý an toàn lao động tại công trường", "Báo cáo định kỳ cho chủ đầu tư", "Hỗ trợ nghiệm thu, thanh quyết toán"],
  steps=["Nhận hồ sơ dự án", "Lập kế hoạch kiểm soát", "Giám sát tại công trường", "Báo cáo định kỳ", "Hỗ trợ nghiệm thu"],
  commit=["Báo cáo tiến độ theo chu kỳ đã thống nhất: %s" % PH("tuần hoặc tháng"), "Kiểm soát vật tư đầu vào trước khi đưa vào công trình", "Hồ sơ nghiệm thu đầy đủ, dễ tra cứu"]),
 dict(id="bao-hanh-bao-tri", ic="shield", name="Bảo hành và bảo trì",
  short="Đồng hành sau bàn giao theo cam kết trong hợp đồng.",
  intro="Công trình bàn giao không phải là điểm dừng. Lộc Minh Anh tiếp nhận và xử lý yêu cầu bảo hành theo hợp đồng và quy định pháp luật.",
  scope=["Bảo hành công trình theo hợp đồng và quy định hiện hành", "Tiếp nhận yêu cầu qua hotline hoặc Zalo", "Kiểm tra định kỳ theo thỏa thuận", "Bảo trì chống thấm, sơn, hệ thống kỹ thuật"],
  steps=["Tiếp nhận yêu cầu", "Kiểm tra hiện trường", "Thống nhất phương án", "Khắc phục", "Xác nhận hoàn tất"],
  commit=["Thời hạn bảo hành ghi rõ trong hợp đồng: %s" % PH("số tháng"), "Phản hồi yêu cầu bảo hành trong %s giờ làm việc" % PH("số giờ"), "Lưu hồ sơ hoàn công và bản vẽ để tra cứu khi cần"]),
]

CATS = [("all", "Tất cả"), ("nha-o", "Nhà ở"), ("thuong-mai", "Thương mại"), ("cong-nghiep", "Công nghiệp"), ("cai-tao", "Cải tạo")]
CATNAME = dict(CATS)
PROJECTS = [
 dict(slug="nha-pho-mau", cat="nha-o", name="Nhà phố [tên dự án]", cover="Ảnh mặt tiền dự án",
  items=["Thiết kế kiến trúc và kết cấu", "Thi công phần thô", "Hoàn thiện nội ngoại thất", "Bảo hành bảo trì"],
  desc="Mẫu trình bày cho nhà phố: mô tả nhu cầu của gia chủ, giải pháp mặt bằng, điểm nhấn mặt tiền và cách Lộc Minh Anh kiểm soát tiến độ. Thay đoạn này bằng thông tin dự án thật."),
 dict(slug="biet-thu-mau", cat="nha-o", name="Biệt thự [tên dự án]", cover="Ảnh phối cảnh dự án",
  items=["Tổng thầu thiết kế – thi công trọn gói", "Cảnh quan, sân vườn", "Nội thất theo thiết kế"],
  desc="Mẫu trình bày cho biệt thự: quy mô, phong cách kiến trúc, vật liệu chính và những thách thức thi công đã xử lý. Thay đoạn này bằng thông tin dự án thật."),
 dict(slug="van-phong-mau", cat="thuong-mai", name="Văn phòng [tên dự án]", cover="Ảnh không gian văn phòng",
  items=["Thi công phần thô và hoàn thiện", "Hệ thống điện, mạng, chiếu sáng", "Vách, trần, sàn", "Bàn giao đúng hạn khai trương"],
  desc="Mẫu trình bày cho công trình văn phòng: yêu cầu về thời gian, cách bố trí công năng và biện pháp thi công không ảnh hưởng hoạt động xung quanh. Thay đoạn này bằng thông tin thật."),
 dict(slug="cua-hang-mau", cat="thuong-mai", name="Cửa hàng – showroom [tên dự án]", cover="Ảnh mặt tiền cửa hàng",
  items=["Thiết kế và thi công trọn gói", "Mặt dựng, biển hiệu", "Hoàn thiện nội thất trưng bày"],
  desc="Mẫu trình bày cho cửa hàng hoặc showroom: nhận diện thương hiệu của chủ đầu tư, tiến độ gấp rút và hạng mục hoàn thiện. Thay đoạn này bằng thông tin dự án thật."),
 dict(slug="nha-xuong-mau", cat="cong-nghiep", name="Nhà xưởng [tên dự án]", cover="Ảnh tổng thể nhà xưởng",
  items=["Móng và sàn công nghiệp", "Khung thép, mái, vách", "Hạ tầng điện, nước, thoát nước", "Sân, đường nội bộ"],
  desc="Mẫu trình bày cho nhà xưởng hoặc kho: tải trọng thiết kế, tiến độ thi công theo giai đoạn và các biện pháp an toàn lao động. Thay đoạn này bằng thông tin dự án thật."),
 dict(slug="cai-tao-nha-mau", cat="cai-tao", name="Cải tạo [tên công trình]", cover="Ảnh trước và sau cải tạo",
  items=["Khảo sát và đánh giá hiện trạng", "Chống thấm, gia cố", "Cải tạo mặt bằng, mặt tiền", "Thay mới điện nước"],
  desc="Mẫu trình bày cho dự án cải tạo: hiện trạng ban đầu, vấn đề cần xử lý, giải pháp và kết quả sau bàn giao. Thay đoạn này bằng thông tin dự án thật."),
]
GALLERY_LABELS = ["Ảnh phối cảnh", "Ảnh mặt tiền", "Ảnh thi công phần thô", "Ảnh hoàn thiện", "Ảnh chi tiết", "Ảnh nội thất"]

PHOTOS = [  # (tệp, rộng, cao, chú thích)
 ("doi-ngu-thi-cong", 1000, 751, "Đội ngũ thi công kiểm tra cốt thép sàn"),
 ("giam-sat-cong-truong", 1000, 751, "Giám sát thi công cốt thép tại công trường"),
 ("thep-san-tang-1", 1000, 751, "Lưới thép sàn trước khi đổ bê tông"),
 ("thep-san-cot", 1000, 751, "Cốt thép sàn quanh chân cột"),
 ("xe-bon-be-tong", 751, 1000, "Xe bồn vận chuyển bê tông đến công trường"),
 ("can-phang-be-tong", 1000, 751, "Cán phẳng bề mặt bê tông"),
 ("mat-duong-be-tong", 751, 1000, "Mặt đường bê tông sau hoàn thiện"),
 ("bao-duong-be-tong", 751, 1000, "Phủ bạt bảo dưỡng bê tông"),
 ("thep-san-nghiem-thu", 1000, 751, "Cốt thép sàn chuẩn bị nghiệm thu"),
 ("xe-bon-san-bai", 751, 1000, "Đổ bê tông sân bãi bằng xe bồn"),
 ("thep-mong-ngoai-troi", 1000, 751, "Cốt thép móng khu vực ngoài trời"),
 ("thep-khu-do-thi", 1000, 751, "Gia công thép nền công trình"),
]

TESTI = [
 ("Báo giá chia theo từng hạng mục nên gia đình tôi dễ so sánh và theo dõi chi phí trong suốt quá trình xây.", "[Tên khách hàng]", "Chủ nhà, [địa điểm]"),
 ("Mỗi giai đoạn đều có biên bản nghiệm thu và ảnh cập nhật, tôi không phải đến công trường liên tục vẫn nắm được tiến độ.", "[Tên khách hàng]", "Chủ đầu tư, [loại công trình]"),
 ("Công trình bàn giao đúng mốc đã ghi trong hợp đồng, những điểm còn tồn đọng được xử lý theo đúng thời hạn đã hẹn.", "[Tên khách hàng]", "Giám đốc, [tên doanh nghiệp]"),
]

POSTS = [
 dict(slug="bao-gia-xay-nha-tron-goi-gom-nhung-gi", title="Báo giá xây nhà trọn gói gồm những gì?",
  desc="Cách đọc bản báo giá xây nhà trọn gói: hạng mục thường được tính, hạng mục hay nằm ngoài báo giá và những câu hỏi cần làm rõ trước khi ký hợp đồng.",
  tag="Báo giá", read="4 phút đọc",
  body="""<p>Cùng gọi là “xây nhà trọn gói” nhưng mỗi bản báo giá có thể bao gồm những phạm vi rất khác nhau. Đọc kỹ báo giá giúp bạn so sánh đúng giữa các nhà thầu và tránh phát sinh về sau.</p>
<h2>Những hạng mục thường nằm trong báo giá trọn gói</h2>
<ul class="checks"><li><b>Thiết kế:</b> bản vẽ kiến trúc, kết cấu, điện nước và hồ sơ phục vụ xin phép xây dựng.</li>
<li><b>Phần thô:</b> nhân công và vật tư cho móng, cột, dầm, sàn, tường, mái, đổ bê tông, xây tô.</li>
<li><b>Phần hoàn thiện:</b> ốp lát, sơn bả, trần, cửa, cầu thang, thiết bị vệ sinh, thiết bị điện theo chủng loại đã thỏa thuận.</li>
<li><b>Quản lý công trình:</b> giám sát, an toàn lao động, vệ sinh công trường.</li>
<li><b>Bảo hành:</b> thời hạn và phạm vi ghi trong hợp đồng.</li></ul>
<h2>Những khoản hay nằm ngoài báo giá</h2>
<p>Hãy hỏi rõ từng khoản dưới đây có được tính hay không, vì đây là nguồn phát sinh phổ biến:</p>
<ul><li>Nội thất rời, đồ gia dụng, điều hòa, thang máy, hệ thống nhà thông minh.</li>
<li>Sân vườn, hồ cá, cổng và hàng rào nếu chưa nằm trong bản vẽ.</li>
<li>Lệ phí xin phép, chi phí đấu nối điện nước, các loại thuế phí theo quy định.</li>
<li>Xử lý nền đất yếu hoặc móng phát sinh khi điều kiện địa chất thực tế khác dự kiến.</li></ul>
<h2>Bốn điểm cần kiểm tra khi đọc báo giá</h2>
<h3>1. Cách tính diện tích</h3><p>Đơn giá theo m² sàn phụ thuộc vào cách quy đổi móng, mái, sân, ban công. Hãy yêu cầu bảng quy đổi bằng văn bản.</p>
<h3>2. Danh mục vật tư</h3><p>Bản báo giá nên ghi tên hãng, quy cách, mã sản phẩm. Cụm “tương đương” cần được định nghĩa rõ.</p>
<h3>3. Điều kiện phát sinh</h3><p>Phát sinh chỉ nên thực hiện khi có báo giá bổ sung và xác nhận của chủ đầu tư bằng văn bản.</p>
<h3>4. Tiến độ thanh toán</h3><p>Các đợt thanh toán nên gắn với giai đoạn đã nghiệm thu, tránh ứng trước quá nhiều so với khối lượng đã hoàn thành.</p>
<p>Nếu bạn đã có bản vẽ hoặc ý tưởng, Lộc Minh Anh có thể lập dự toán chi tiết theo từng hạng mục để bạn dễ đối chiếu.</p>"""),
 dict(slug="cac-buoc-xin-phep-xay-dung", title="Các bước xin phép xây dựng nhà ở",
  desc="Tổng quan các bước xin giấy phép xây dựng nhà ở riêng lẻ: xác định có cần xin phép không, chuẩn bị giấy tờ, bản vẽ, nộp hồ sơ và nhận kết quả.",
  tag="Thủ tục", read="4 phút đọc",
  body="""<p class="note">Quy định về cấp phép xây dựng và cơ quan tiếp nhận hồ sơ có thể thay đổi theo từng thời kỳ và địa phương. Bài viết chỉ mang tính tham khảo chung, bạn nên xác nhận với cơ quan có thẩm quyền nơi xây dựng.</p>
<h2>Bước 1. Xác định có cần xin phép không</h2>
<p>Pháp luật xây dựng quy định một số trường hợp được miễn giấy phép, ví dụ một số nhà ở riêng lẻ ở khu vực nông thôn đáp ứng điều kiện quy định. Dù được miễn, công trình vẫn phải tuân thủ quy hoạch và các yêu cầu an toàn. Hãy hỏi cơ quan quản lý xây dựng tại địa phương để biết chính xác trường hợp của bạn.</p>
<h2>Bước 2. Chuẩn bị giấy tờ về đất</h2>
<p>Thông thường cần giấy chứng nhận quyền sử dụng đất, quyền sở hữu nhà ở và tài sản khác gắn liền với đất, hoặc giấy tờ hợp pháp tương đương theo quy định.</p>
<h2>Bước 3. Thiết kế bản vẽ</h2>
<p>Bản vẽ gồm mặt bằng, mặt đứng, mặt cắt, thiết kế móng và sơ đồ đấu nối hạ tầng. Nên giao cho đơn vị thiết kế có đủ năng lực và hiểu yêu cầu của địa phương.</p>
<h2>Bước 4. Lập hồ sơ xin phép</h2>
<ul class="checks"><li>Đơn đề nghị cấp giấy phép xây dựng theo mẫu.</li><li>Giấy tờ về quyền sử dụng đất.</li><li>Bản vẽ thiết kế đã hoàn chỉnh.</li><li>Các giấy tờ bổ sung theo yêu cầu của cơ quan cấp phép, ví dụ cam kết bảo đảm an toàn cho công trình liền kề khi có tầng hầm.</li></ul>
<h2>Bước 5. Nộp hồ sơ và theo dõi kết quả</h2>
<p>Nộp hồ sơ tại cơ quan có thẩm quyền theo phân cấp hiện hành ở địa phương, trực tiếp hoặc qua cổng dịch vụ công nếu có. Giữ biên nhận để theo dõi thời hạn xử lý.</p>
<h2>Bước 6. Trước khi khởi công</h2>
<p>Nhận giấy phép, thông báo khởi công theo quy định, treo biển công trình và lưu bản giấy phép tại công trường. Nên ký hợp đồng thi công với nhà thầu sau khi hồ sơ thiết kế đã được chốt.</p>
<p>Lộc Minh Anh có thể hỗ trợ thiết kế và chuẩn bị hồ sơ để bạn tiết kiệm thời gian ở bước này.</p>"""),
 dict(slug="cach-chon-nha-thau-xay-dung", title="Cách chọn nhà thầu xây dựng đáng tin cậy",
  desc="Sáu tiêu chí giúp chủ nhà và chủ đầu tư chọn nhà thầu xây dựng: pháp lý, công trình thực tế, hợp đồng, báo giá, giám sát và bảo hành.",
  tag="Kinh nghiệm", read="5 phút đọc",
  body="""<p>Chọn nhà thầu là quyết định ảnh hưởng đến chi phí, tiến độ và độ bền của công trình. Dưới đây là sáu tiêu chí bạn có thể dùng để so sánh.</p>
<h2>1. Hồ sơ pháp lý và năng lực</h2><p>Đề nghị xem giấy đăng ký kinh doanh và chứng chỉ năng lực hoạt động xây dựng phù hợp quy mô công trình của bạn.</p>
<h2>2. Công trình thực tế</h2><p>Xem công trình đã bàn giao hoặc đang thi công, nếu có thể hãy trao đổi với chủ nhà trước đó về tiến độ, thái độ xử lý phát sinh và bảo hành.</p>
<h2>3. Hợp đồng rõ ràng</h2><p>Hợp đồng cần nêu phạm vi công việc, danh mục vật tư, tiến độ, các đợt thanh toán, điều khoản xử lý chậm tiến độ, phát sinh và bảo hành.</p>
<h2>4. Báo giá minh bạch</h2><p>Báo giá bóc tách theo hạng mục giúp bạn kiểm soát chi phí và dễ đối chiếu giữa các nhà thầu.</p>
<h2>5. Đội ngũ và giám sát tại công trường</h2><p>Hỏi ai là chỉ huy trưởng, cách báo cáo tiến độ, quy định an toàn lao động và biện pháp giữ vệ sinh khu vực xung quanh.</p>
<h2>6. Chính sách bảo hành</h2><p>Thời hạn bảo hành, phạm vi và cách tiếp nhận yêu cầu nên được ghi trong hợp đồng.</p>
<h2>Những dấu hiệu cần thận trọng</h2>
<ul><li>Giá thấp bất thường so với các báo giá còn lại mà không giải thích được.</li><li>Yêu cầu ứng trước một khoản lớn khi chưa có hợp đồng.</li><li>Báo giá chung chung, không có danh mục vật tư.</li><li>Cam kết mơ hồ, không đưa vào hợp đồng.</li></ul>
<p>Đây cũng là những tiêu chí Lộc Minh Anh tự áp dụng khi làm việc với khách hàng: nói bằng cam kết cụ thể trong hợp đồng.</p>"""),
]

JOBS = [("Chỉ huy trưởng công trình", "Điều hành thi công, tiến độ, an toàn tại công trường."),
        ("Kỹ sư giám sát – dự toán", "Giám sát chất lượng, bóc tách khối lượng, lập dự toán."),
        ("Kỹ sư thiết kế kiến trúc – kết cấu", "Lập hồ sơ thiết kế, làm việc trực tiếp với khách hàng.")]

# ---------------------------------------------------------------- khung trang
CONTACT_DEFAULT = PH("cập nhật")

def schema_org():
    return json.dumps({"@context": "https://schema.org", "@type": ["GeneralContractor", "LocalBusiness"],
        "name": "Lộc Minh Anh", "alternateName": "LMA", "slogan": SLOGAN, "url": BASE,
        "logo": BASE + "assets/img/logo-lma.png", "image": BASE + "assets/img/og-image.jpg",
        "description": "Công ty tổng thầu xây dựng khu vực miền Trung, Việt Nam: thiết kế – thi công trọn gói, dân dụng và công nghiệp, hoàn thiện, cải tạo, quản lý dự án, bảo hành bảo trì.",
        "areaServed": "Miền Trung, Việt Nam", "address": {"@type": "PostalAddress", "addressCountry": "VN"}},
        ensure_ascii=False)

def page(file, title, desc, main, active="", schema=None, og_type="website", lightbox=False):
    depth = file.count("/")
    R = "../" * depth
    url = BASE + file.replace("index.html", "")
    nav = "".join('<li><a href="@/%s"%s>%s</a></li>' % (h, ' aria-current="page"' if h == active else "", t) for t, h in NAV)
    ld = '<script type="application/ld+json">%s</script>\n' % schema if schema else ""
    lbx = ('<dialog class="lb" id="lb" aria-label="Xem ảnh phóng to"><figure><button class="x" type="button" aria-label="Đóng">×</button>'
           '<button class="pv" type="button" aria-label="Ảnh trước">‹</button><img alt="" src=""><figcaption></figcaption>'
           '<button class="nx" type="button" aria-label="Ảnh sau">›</button></figure></dialog>') if lightbox else ""
    out = """<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>%(title)s</title>
<meta name="description" content="%(desc)s">
<meta name="theme-color" content="#0E2F7A">
<link rel="canonical" href="%(url)s">
<meta property="og:type" content="%(og)s"><meta property="og:locale" content="vi_VN"><meta property="og:site_name" content="Lộc Minh Anh">
<meta property="og:title" content="%(title)s"><meta property="og:description" content="%(desc)s">
<meta property="og:url" content="%(url)s"><meta property="og:image" content="%(base)sassets/img/og-image.jpg">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" type="image/png" href="@/assets/img/favicon.png"><link rel="apple-touch-icon" href="@/assets/img/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:wght@400;500;600;800&amp;display=swap">
<link rel="stylesheet" href="@/style.css">
<script>document.documentElement.classList.add('js')</script>
%(ld)s</head>
<body>
<a class="skip" href="#main">Bỏ qua điều hướng</a>
<header class="site-header"><div class="wrap">
<a class="brand" href="@/index.html" aria-label="Lộc Minh Anh – về trang chủ"><span class="mark"><img src="@/assets/img/logo-mark.png" width="625" height="392" alt="Biểu tượng LMA"></span><span class="brand-name">LỘC MINH ANH</span></a>
<nav class="nav" id="nav" aria-label="Điều hướng chính"><ul>%(nav)s</ul></nav>
<a class="btn btn-gold btn-sm header-cta" href="@/lien-he.html#bao-gia">Nhận tư vấn dự án</a>
<button class="menu-btn" type="button" aria-expanded="false" aria-controls="nav" aria-label="Mở menu">%(menu)s</button>
</div></header>
<main id="main">
%(main)s
</main>
<footer class="site-footer"><div class="wrap">
<div><a class="brand-full" href="@/index.html" aria-label="Lộc Minh Anh – về trang chủ"><img src="@/assets/img/logo-lma.png" width="730" height="640" alt="Logo Lộc Minh Anh" loading="lazy"></a>
<p style="margin-top:14px"><b>Công ty Lộc Minh Anh</b><br>Tổng thầu xây dựng khu vực miền Trung</p>
<p>%(slogan)s</p></div>
<div><h2>Liên kết</h2><ul>
<li><a href="@/gioi-thieu.html">Giới thiệu</a></li><li><a href="@/dich-vu.html">Dịch vụ</a></li><li><a href="@/du-an.html">Dự án</a></li>
<li><a href="@/quy-trinh.html">Quy trình và cam kết</a></li><li><a href="@/tin-tuc.html">Tin tức</a></li><li><a href="@/tuyen-dung.html">Tuyển dụng</a></li><li><a href="@/lien-he.html">Liên hệ</a></li></ul></div>
<div><h2>Thông tin công ty</h2>
<p>Địa chỉ: <span data-lma="address">[cập nhật]</span></p>
<p>Hotline: <a href="@/lien-he.html" data-lma="hotline">[cập nhật]</a></p>
<p>Email: <a href="@/lien-he.html" data-lma="email">[cập nhật]</a></p>
<p>Giờ làm việc: <span data-lma="hours">[cập nhật]</span></p></div>
<div><h2>Kết nối</h2><ul>
<li><a href="@/lien-he.html" data-lma="facebook">Facebook Lộc Minh Anh</a></li>
<li><a href="@/lien-he.html" data-lma="zalo">Chat Zalo</a></li>
<li><a href="@/lien-he.html#bao-gia">Nhận báo giá</a></li></ul></div>
<div class="copy"><span>© 2026 Công ty Lộc Minh Anh. Bảo lưu mọi quyền.</span><span>Mã số thuế: [cập nhật]</span></div>
</div></footer>
<div class="fab" aria-label="Liên hệ nhanh">
<a class="zalo" href="@/lien-he.html" data-lma="zalo" aria-label="Nhắn Zalo cho Lộc Minh Anh">Zalo</a>
<a class="call" href="@/lien-he.html" data-lma="hotline" data-text="no" aria-label="Gọi hotline Lộc Minh Anh">%(phone)s</a>
</div>
%(lbx)s
<script src="@/script.js" defer></script>
</body>
</html>
""" % dict(title=esc(title), desc=esc(desc, quote=True), url=url, og=og_type, base=BASE, ld=ld, nav=nav, menu=IC["menu"],
           main=main, slogan=SLOGAN, phone=IC["phone"], lbx=lbx)
    out = out.replace("@/", R)
    p = ROOT / file
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(out, encoding="utf-8")

def hero_page(h1, lead, crumbs):
    cr = " / ".join(crumbs)
    return ('<div class="page-hero"><div class="wrap"><p class="crumb">%s</p><h1>%s</h1><p class="lead">%s</p></div></div>' % (cr, h1, lead))
HOME = '<a href="@/index.html">Trang chủ</a>'

def cta_band(title="Bạn đang có dự án cần triển khai?", text="Gửi nhu cầu của bạn, Lộc Minh Anh sẽ liên hệ để khảo sát và lập báo giá chi tiết."):
    return ('<section class="band-navy"><div class="wrap center rv"><h2>%s</h2><p class="lead">%s</p>'
            '<div class="btns" style="justify-content:center"><a class="btn btn-gold" href="@/lien-he.html#bao-gia">Nhận tư vấn dự án</a>'
            '<a class="btn btn-line" href="@/du-an.html">Xem dự án</a></div></div></section>' % (title, text))

def gallery(photos, hint=""):
    b = ""
    for f, w, h, cap in photos:
        b += ('<button type="button" data-lb="@/assets/img/site/%s.jpg" data-alt="%s"><img src="@/assets/img/site/%s.jpg" width="%d" height="%d" loading="lazy" alt="%s"><span class="cap">%s</span></button>'
              % (f, esc(cap, True), f, w, h, esc(cap, True), esc(cap)))
    return '<div class="gal rv">%s</div>' % b

def svc_card(s):
    return ('<article class="card rv"><div class="ico">%s</div><h3>%s</h3><p>%s</p><a class="more" href="@/dich-vu.html#%s">Xem chi tiết<span class="sr"> %s</span> →</a></article>'
            % (IC[s["ic"]], s["name"], s["short"], s["id"], esc(s["name"])))

def proj_card(p, link="@/du-an/%s.html"):
    return ('<a class="pcard rv" href="%s" data-cat="%s"><div class="ph"><span>%s</span></div><span class="tag">%s</span><h3>%s</h3><p class="meta">Loại hình: %s · Địa điểm: [địa điểm] · Năm: [năm]</p></a>'
            % (link % p["slug"], p["cat"], p["cover"], CATNAME[p["cat"]], esc(p["name"]), CATNAME[p["cat"]]))

STEPS5 = [("Tiếp nhận", "Nghe nhu cầu, khảo sát hiện trạng."), ("Thiết kế và báo giá", "Phương án, dự toán chi tiết."),
          ("Ký hợp đồng", "Chốt phạm vi, tiến độ, thanh toán."), ("Thi công", "Báo cáo định kỳ, nghiệm thu theo giai đoạn."),
          ("Bàn giao", "Hoàn công, bảo hành, bảo trì.")]
def steps5(dark=False):
    return '<ol class="steps">%s</ol>' % "".join('<li class="rv"><span class="num">%02d</span><h3>%s</h3><p>%s</p></li>' % (i + 1, t, d) for i, (t, d) in enumerate(STEPS5))

# ---------------------------------------------------------------- TRANG CHỦ
def build_home():
    hero = """<section class="hero"><div class="wrap">
<div class="rv"><span class="kicker">Tổng thầu xây dựng · Miền Trung</span>
<h1>%s</h1>
<p class="lead">Lộc Minh Anh nhận trọn gói từ thiết kế, thi công đến hoàn thiện công trình. Một đầu mối chịu trách nhiệm, tiến độ và chất lượng được cam kết rõ ràng trong hợp đồng.</p>
<div class="btns"><a class="btn btn-gold" href="@/lien-he.html#bao-gia">Nhận tư vấn dự án</a><a class="btn btn-line" href="@/du-an.html">Xem dự án</a></div>
<ul class="trust"><li>Một đầu mối chịu trách nhiệm</li><li>Báo giá bóc tách theo hạng mục</li><li>Tiến độ ghi trong hợp đồng</li></ul></div>
<div class="hero-art rv"><div class="logo-card"><img src="@/assets/img/logo-lma.png" width="730" height="640" alt="Logo Lộc Minh Anh – LMA, Vững bền kiến tạo tương lai" fetchpriority="high"></div></div>
</div></section>""" % SLOGAN

    intro = """<section id="gioi-thieu"><div class="wrap split">
<div class="rv"><span class="kicker">Giới thiệu</span><h2>Một đầu mối cho cả công trình</h2>
<p class="lead">Chúng tôi không chỉ thi công. Lộc Minh Anh điều phối thiết kế, vật tư, nhân lực và an toàn để chủ đầu tư yên tâm với một hợp đồng và một đội ngũ chịu trách nhiệm.</p>
<ul class="checks"><li>Tầm nhìn: trở thành nhà tổng thầu đáng tin cậy của khách hàng miền Trung.</li><li>Sứ mệnh: kiến tạo công trình an toàn, đúng tiến độ, bền vững theo thời gian.</li><li>Giá trị cốt lõi: Uy tín · Chất lượng · Đúng tiến độ · An toàn · Đồng hành lâu dài.</li></ul>
<a class="btn btn-line" href="@/gioi-thieu.html">Tìm hiểu về LMA</a></div>
<figure class="photo rv" style="margin:0"><img src="@/assets/img/site/doi-ngu-thi-cong.jpg" width="1000" height="751" loading="lazy" alt="Đội ngũ thi công kiểm tra cốt thép sàn tại công trường"></figure>
</div></section>"""

    svc = ('<section class="alt" id="dich-vu"><div class="wrap"><div class="sec-head rv"><span class="kicker">Dịch vụ nổi bật</span><h2>Từ ý tưởng đến bàn giao</h2>'
           '<p class="lead">Lộc Minh Anh nhận trọn gói hoặc theo từng gói thầu, tùy nhu cầu của chủ đầu tư.</p></div><div class="grid g3">%s</div></div></section>'
           % "".join(svc_card(s) for s in SERVICES))

    proc = ('<section class="band-navy" id="quy-trinh"><div class="wrap"><div class="sec-head rv"><span class="kicker">Quy trình 5 bước</span><h2>Làm việc minh bạch từng bước</h2>'
            '<p class="lead">Mỗi giai đoạn có đầu ra rõ ràng để chủ đầu tư theo dõi và nghiệm thu.</p></div>%s'
            '<div class="btns"><a class="btn btn-gold" href="@/quy-trinh.html">Xem chi tiết quy trình</a></div></div></section>' % steps5())

    proj = ('<section id="du-an"><div class="wrap"><div class="sec-head rv"><span class="kicker">Dự án tiêu biểu</span><h2>Công trình tiêu biểu</h2>'
            '<p class="lead">Các khung dưới đây là dự án mẫu. Thay bằng ảnh và thông tin công trình thật của Lộc Minh Anh.</p></div>'
            '<div class="grid g3">%s</div><div class="btns"><a class="btn btn-line" href="@/du-an.html">Xem tất cả dự án</a></div></div></section>'
            % "".join(proj_card(p) for p in PROJECTS[:3]))

    log = ('<section class="alt"><div class="wrap"><div class="sec-head rv"><span class="kicker">Nhật ký công trường</span><h2>Hình ảnh thi công thực tế</h2>'
           '<p class="lead">Cốt thép, đổ và bảo dưỡng bê tông: những công đoạn quyết định độ bền của công trình, được ghi lại tại hiện trường.</p></div>%s'
           '<div class="btns"><a class="btn btn-line" href="@/du-an.html#cong-truong">Xem thêm ảnh công trường</a></div></div></section>' % gallery(PHOTOS[:8]))

    why = [("handshake", "Một đầu mối trọn gói", "Thiết kế, thi công, hoàn thiện và bảo hành do cùng một đội ngũ chịu trách nhiệm."),
           ("doc", "Minh bạch chi phí", "Dự toán bóc tách theo hạng mục. Phát sinh chỉ thực hiện khi bạn xác nhận bằng văn bản."),
           ("calendar", "Đúng tiến độ", "Mốc tiến độ ghi trong hợp đồng, theo dõi bằng báo cáo định kỳ."),
           ("helmet", "An toàn công trường", "Quy định an toàn lao động và che chắn khu vực xung quanh được thực hiện từ ngày khởi công."),
           ("eye", "Nghiệm thu từng giai đoạn", "Cốt thép, bê tông, hoàn thiện đều có biên bản trước khi sang bước tiếp theo."),
           ("shield", "Đồng hành sau bàn giao", "Tiếp nhận bảo hành, bảo trì theo cam kết trong hợp đồng.")]
    whys = ('<section id="ly-do"><div class="wrap"><div class="sec-head rv"><span class="kicker">Vì sao chọn LMA</span><h2>Sáu cam kết chúng tôi theo đuổi</h2></div><div class="grid g3">%s</div></div></section>'
            % "".join('<article class="card rv"><div class="ico">%s</div><h3>%s</h3><p>%s</p></article>' % (IC[i], t, d) for i, t, d in why))

    tes = ('<section class="alt"><div class="wrap"><div class="sec-head rv"><span class="kicker">Khách hàng nói gì</span><h2>Phản hồi từ chủ đầu tư</h2>'
           '<p class="note">Nội dung mẫu, thay bằng phản hồi thật của khách hàng.</p></div><div class="grid g3">%s</div></div></section>'
           % "".join('<figure class="card quote rv" style="margin:0"><blockquote>%s</blockquote><figcaption><cite>%s</cite><span class="meta-line">%s</span><span class="sample">Nội dung mẫu, thay bằng phản hồi thật</span></figcaption></figure>' % t for t in TESTI))

    page("index.html", "Lộc Minh Anh – Tổng thầu xây dựng miền Trung | Vững bền kiến tạo tương lai",
         "Lộc Minh Anh nhận tổng thầu thiết kế – thi công trọn gói, xây dựng dân dụng và công nghiệp tại miền Trung. Một đầu mối, tiến độ và chi phí minh bạch. Nhận tư vấn dự án.",
         hero + intro + svc + proc + proj + log + whys + tes + cta_band(), active="index.html", schema=schema_org(), lightbox=True)

# ---------------------------------------------------------------- GIỚI THIỆU
def build_about():
    vals = [("Uy tín", "Nói được thì làm được, mọi cam kết đều nằm trong hợp đồng."), ("Chất lượng", "Kiểm soát vật tư và nghiệm thu từng công đoạn."),
            ("Đúng tiến độ", "Mốc thời gian rõ ràng, báo cáo định kỳ."), ("An toàn", "An toàn lao động và an toàn cho khu vực xung quanh."),
            ("Đồng hành lâu dài", "Có mặt cả sau khi bàn giao.")]
    main = hero_page("Về Lộc Minh Anh", "Công ty tổng thầu xây dựng khu vực miền Trung. Chúng tôi làm việc bằng cam kết cụ thể: tiến độ, chất lượng và chi phí rõ ràng trong từng hợp đồng.", [HOME, "Giới thiệu"])
    main += """<section><div class="wrap split"><div class="rv"><span class="kicker">Câu chuyện công ty</span><h2>Làm công trình theo cách dễ hiểu và dễ kiểm chứng</h2>
<p>Lộc Minh Anh theo đuổi một cách làm đơn giản: chủ đầu tư chỉ cần làm việc với một đầu mối, hiểu rõ mình đang trả tiền cho hạng mục nào, và biết công trình đang ở giai đoạn nào.</p>
<p>Từ thiết kế, dự toán, thi công đến bảo hành, mỗi bước đều có hồ sơ, biên bản và người chịu trách nhiệm cụ thể.</p>
<p class="note">Thông tin thành lập: %s %s %s. Bổ sung câu chuyện thật của công ty tại đây.</p></div>
<figure class="photo rv" style="margin:0"><img src="@/assets/img/site/giam-sat-cong-truong.jpg" width="1000" height="751" loading="lazy" alt="Giám sát thi công cốt thép tại công trường"></figure></div></section>""" % (PH("năm thành lập"), PH("người sáng lập"), PH("địa bàn hoạt động"))
    main += """<section class="alt"><div class="wrap"><div class="grid g2">
<article class="card rv"><span class="num">TẦM NHÌN</span><h3>Nhà tổng thầu đáng tin cậy</h3><p>Trở thành nhà tổng thầu xây dựng được khách hàng miền Trung tin tưởng nhờ những công trình bàn giao đúng cam kết.</p></article>
<article class="card rv"><span class="num">SỨ MỆNH</span><h3>Công trình bền theo thời gian</h3><p>Kiến tạo những công trình an toàn, đúng tiến độ, bền vững theo thời gian và minh bạch chi phí cho mọi khách hàng.</p></article></div></div></section>"""
    main += ('<section><div class="wrap"><div class="sec-head rv"><span class="kicker">Giá trị cốt lõi</span><h2>Năm giá trị định hướng mọi quyết định</h2></div><div class="grid g3">%s</div></div></section>'
             % "".join('<article class="card rv"><span class="num">%02d</span><h3>%s</h3><p>%s</p></article>' % (i + 1, t, d) for i, (t, d) in enumerate(vals)))
    main += """<section class="alt"><div class="wrap split"><div class="rv"><div class="logo-card" style="margin:auto"><img src="@/assets/img/logo-lma.png" width="730" height="640" alt="Logo Lộc Minh Anh" loading="lazy"></div></div>
<div class="rv"><span class="kicker">Ý nghĩa logo</span><h2>Biểu tượng của sự vững chắc và an cư</h2>
<ul class="checks"><li><b>Chữ LMA:</b> bộ chữ cái viết tắt của Lộc Minh Anh, dựng khối chắc chắn.</li>
<li><b>Cụm tòa nhà:</b> quy mô và năng lực thi công công trình.</li>
<li><b>Ngôi nhà:</b> sự an cư, mục tiêu cuối cùng của mỗi công trình.</li>
<li><b>Vòng cung xanh:</b> sự kết nối và trọn vẹn giữa khách hàng và nhà thầu.</li>
<li><b>Màu vàng và xanh:</b> vàng là “Lộc” thịnh vượng, xanh dương là sự vững chắc.</li></ul></div></div></section>"""
    stats = [("số năm", "Năm kinh nghiệm"), ("số dự án", "Dự án đã bàn giao"), ("số kỹ sư", "Kỹ sư và chuyên viên"), ("số lượng", "Chứng chỉ năng lực")]
    main += ('<section><div class="wrap"><div class="sec-head rv"><span class="kicker">Năng lực và đội ngũ</span><h2>Con số sẽ được cập nhật bằng dữ liệu thật</h2>'
             '<p class="lead">Các ô dưới đây giữ chỗ cho số liệu thực tế của công ty. Chúng tôi không tự đặt con số khi chưa có xác nhận.</p></div><div class="grid g4">%s</div>'
             '<h3 style="margin-top:44px" class="rv">Đội ngũ chủ chốt</h3><div class="grid g3">%s</div></div></section>'
             % ("".join('<div class="card rv center"><div style="font-size:1.7rem;font-weight:800">%s</div><p style="margin:6px 0 0">%s</p></div>' % (PH(a), b) for a, b in stats),
                "".join('<div class="card rv"><div class="ph" style="aspect-ratio:1/1;margin-bottom:14px"><span>Ảnh chân dung</span></div><h3>[Họ và tên]</h3><p>%s</p></div>' % r for r in ["Giám đốc điều hành", "Giám đốc kỹ thuật", "Chỉ huy trưởng công trình"])))
    main += cta_band()
    page("gioi-thieu.html", "Giới thiệu – Lộc Minh Anh | Tổng thầu xây dựng miền Trung",
         "Câu chuyện, tầm nhìn, sứ mệnh, giá trị cốt lõi, ý nghĩa logo và năng lực của Lộc Minh Anh, công ty tổng thầu xây dựng khu vực miền Trung.", main, active="gioi-thieu.html")

# ---------------------------------------------------------------- DỊCH VỤ
def build_services():
    main = hero_page("Dịch vụ tổng thầu xây dựng", "Sáu nhóm dịch vụ có thể nhận trọn gói hoặc theo từng gói thầu, mỗi nhóm đều có phạm vi, quy trình và cam kết cụ thể.", [HOME, "Dịch vụ"])
    main += '<section><div class="wrap"><h2 class="sr">Các nhóm dịch vụ</h2><div class="grid g3">%s</div></div></section>' % "".join(svc_card(s) for s in SERVICES)
    for i, s in enumerate(SERVICES):
        main += ('<section id="%s" class="%s"><div class="wrap"><div class="sec-head rv"><span class="kicker">Dịch vụ %02d</span><h2>%s</h2><p class="lead">%s</p></div>'
                 '<div class="grid g3"><div class="card rv"><h3>Phạm vi công việc</h3><ul class="checks">%s</ul></div>'
                 '<div class="card rv"><h3>Quy trình</h3><ol>%s</ol></div>'
                 '<div class="card rv"><h3>Cam kết</h3><ul class="checks">%s</ul></div></div></div></section>'
                 % (s["id"], "alt" if i % 2 == 0 else "", i + 1, s["name"], s["intro"],
                    "".join("<li>%s</li>" % x for x in s["scope"]), "".join("<li>%s</li>" % x for x in s["steps"]), "".join("<li>%s</li>" % x for x in s["commit"])))
    main += cta_band("Chưa chắc nên chọn gói dịch vụ nào?", "Hãy mô tả công trình của bạn, chúng tôi sẽ đề xuất phạm vi phù hợp và báo giá chi tiết.")
    page("dich-vu.html", "Dịch vụ – Tổng thầu thiết kế, thi công trọn gói | Lộc Minh Anh",
         "Dịch vụ của Lộc Minh Anh: tổng thầu thiết kế – thi công trọn gói, xây dựng dân dụng và công nghiệp, hoàn thiện nội ngoại thất, cải tạo sửa chữa, quản lý dự án, bảo hành bảo trì.", main, active="dich-vu.html")

# ---------------------------------------------------------------- DỰ ÁN
def build_projects():
    main = hero_page("Dự án tiêu biểu", "Lọc theo loại hình để xem các công trình nhà ở, thương mại, công nghiệp và cải tạo.", [HOME, "Dự án"])
    main += ('<section><div class="wrap"><h2 class="sr">Danh sách dự án</h2><div class="filters" role="group" aria-label="Lọc dự án theo loại hình">%s</div>'
             '<p class="meta-line" id="fcount" aria-live="polite">%d dự án</p><div class="grid g3">%s</div>'
             '<p class="note">Các dự án trên là dự án mẫu. Thay tên, địa điểm, quy mô, năm và ảnh bằng thông tin thật.</p></div></section>'
             % ("".join('<button type="button" data-filter="%s" aria-pressed="%s">%s</button>' % (k, "true" if k == "all" else "false", v) for k, v in CATS),
                len(PROJECTS), "".join(proj_card(p, "@/du-an/%s.html") for p in PROJECTS)))
    main += ('<section class="alt" id="cong-truong"><div class="wrap"><div class="sec-head rv"><span class="kicker">Nhật ký công trường</span><h2>Hình ảnh thi công thực tế</h2>'
             '<p class="lead">Bấm vào ảnh để xem lớn. Khi có thông tin từng dự án, ảnh sẽ được gắn vào đúng trang dự án.</p></div>%s</div></section>' % gallery(PHOTOS))
    main += cta_band()
    page("du-an.html", "Dự án – Công trình tiêu biểu | Lộc Minh Anh",
         "Dự án tiêu biểu của Lộc Minh Anh: nhà ở, thương mại, công nghiệp, cải tạo. Xem loại hình, quy mô, hạng mục và hình ảnh thi công thực tế.", main, active="du-an.html", lightbox=True)
    for p in PROJECTS:
        gal = "".join('<div class="ph rv"><span>%s</span></div>' % l for l in GALLERY_LABELS)
        facts = "".join("<div><dt>%s</dt><dd>%s</dd></div>" % (a, b) for a, b in [("Loại hình", CATNAME[p["cat"]]), ("Địa điểm", "[địa điểm]"), ("Quy mô", "[diện tích / số tầng]"), ("Năm thực hiện", "[năm]"), ("Chủ đầu tư", "[tên chủ đầu tư]")])
        m = hero_page(esc(p["name"]), "Loại hình %s · Dự án mẫu, thay bằng thông tin thật." % CATNAME[p["cat"]].lower(), [HOME, '<a href="@/du-an.html">Dự án</a>', esc(p["name"])])
        m += ('<section><div class="wrap split"><div class="rv"><div class="ph"><span>%s</span></div></div><div class="rv"><h2>Thông tin dự án</h2><dl class="facts">%s</dl></div></div></section>'
              '<section class="alt"><div class="wrap split"><div class="rv"><span class="kicker">Mô tả</span><h2>Về dự án</h2><p>%s</p></div>'
              '<div class="rv"><h3>Hạng mục thực hiện</h3><ul class="checks">%s</ul></div></div></section>'
              '<section><div class="wrap"><div class="sec-head rv"><span class="kicker">Thư viện ảnh</span><h2>Hình ảnh dự án</h2></div><div class="grid g3">%s</div>'
              '<div class="btns"><a class="btn btn-line" href="@/du-an.html">← Tất cả dự án</a></div></div></section>'
              % (p["cover"], facts, esc(p["desc"]), "".join("<li>%s</li>" % x for x in p["items"]), gal)) + cta_band()
        page("du-an/%s.html" % p["slug"], "%s – Dự án | Lộc Minh Anh" % p["name"],
             "Dự án mẫu %s của Lộc Minh Anh: địa điểm, quy mô, năm thực hiện, hạng mục và thư viện ảnh." % p["name"], m, active="du-an.html")

# ---------------------------------------------------------------- QUY TRÌNH
def build_process():
    det = [("Tiếp nhận và khảo sát", "Lắng nghe nhu cầu, ngân sách và mốc thời gian mong muốn. Khảo sát hiện trạng khu đất hoặc công trình.", ["Biên bản khảo sát và yêu cầu", "Định hướng phương án sơ bộ"]),
           ("Thiết kế và báo giá", "Lập phương án kiến trúc, kết cấu và dự toán theo từng hạng mục để bạn dễ so sánh.", ["Bản vẽ thiết kế", "Bảng dự toán chi tiết, danh mục vật tư"]),
           ("Ký hợp đồng", "Chốt phạm vi công việc, tiến độ, các đợt thanh toán, điều khoản bảo hành.", ["Hợp đồng trọn gói", "Phụ lục vật tư và kế hoạch tiến độ"]),
           ("Thi công và giám sát", "Thi công theo bản vẽ, nghiệm thu từng giai đoạn, cập nhật tiến độ định kỳ cho chủ đầu tư.", ["Biên bản nghiệm thu từng giai đoạn", "Báo cáo, ảnh tiến độ và nhật ký công trình"]),
           ("Bàn giao và bảo hành", "Nghiệm thu tổng thể, hoàn công, hướng dẫn sử dụng. Tiếp nhận bảo hành, bảo trì theo hợp đồng.", ["Hồ sơ hoàn công", "Biên bản bàn giao và phiếu bảo hành"])]
    main = hero_page("Quy trình làm việc và cam kết", "Năm bước rõ ràng, mỗi bước đều có đầu ra bạn có thể kiểm tra và nghiệm thu.", [HOME, "Quy trình"])
    main += ('<section><div class="wrap"><ol class="steps-detail">%s</ol></div></section>'
             % "".join('<li class="rv"><div class="big">%02d</div><div><h2 style="font-size:1.35rem">%s</h2><p>%s</p></div><div><b>Bạn nhận được</b><ul class="checks" style="margin-top:8px">%s</ul></div></li>'
                       % (i + 1, t, d, "".join("<li>%s</li>" % x for x in o)) for i, (t, d, o) in enumerate(det)))
    main += ('<section class="alt" id="cam-ket"><div class="wrap"><div class="sec-head rv"><span class="kicker">Cam kết</span><h2>Ba cam kết ghi trong hợp đồng</h2></div><div class="grid g3">'
             '<article class="card rv"><div class="ico">%s</div><h3>Tiến độ</h3><p>Mốc khởi công, các mốc nghiệm thu và ngày bàn giao được ghi rõ. Chậm tiến độ do nhà thầu được xử lý theo điều khoản đã thỏa thuận.</p></article>'
             '<article class="card rv"><div class="ico">%s</div><h3>Chất lượng</h3><p>Thi công đúng bản vẽ, vật tư đúng chủng loại trong phụ lục, nghiệm thu từng công đoạn có biên bản.</p></article>'
             '<article class="card rv"><div class="ico">%s</div><h3>Bảo hành</h3><p>Thời hạn bảo hành %s, tiếp nhận yêu cầu qua hotline và Zalo, khắc phục theo phương án thống nhất.</p></article></div></div></section>'
             % (IC["calendar"], IC["eye"], IC["shield"], PH("số tháng")))
    faq = [("Chi phí phát sinh được xử lý thế nào?", "Hạng mục ngoài hợp đồng được lập báo giá bổ sung và chỉ thi công khi chủ đầu tư xác nhận bằng văn bản."),
           ("Tôi có theo dõi được tiến độ không?", "Có. Chúng tôi gửi báo cáo định kỳ kèm ảnh, mời chủ đầu tư tham gia nghiệm thu từng giai đoạn."),
           ("Việc thanh toán chia thế nào?", "Chia theo các giai đoạn nghiệm thu ghi trong hợp đồng. Tỷ lệ cụ thể được thỏa thuận theo từng dự án."),
           ("Bảo hành gồm những gì?", "Theo hợp đồng và quy định pháp luật về bảo hành công trình xây dựng. Phạm vi và thời hạn được ghi rõ khi ký."),
           ("Tôi đã có bản vẽ, LMA có thi công được không?", "Được. Chúng tôi nhận thi công theo bản vẽ có sẵn, hoặc rà soát bản vẽ và lập dự toán trước khi ký hợp đồng.")]
    main += ('<section><div class="wrap" style="max-width:820px"><div class="sec-head rv"><span class="kicker">Câu hỏi thường gặp</span><h2>Những điều chủ đầu tư hay hỏi</h2></div>%s</div></section>'
             % "".join("<details class='rv'><summary>%s</summary><p>%s</p></details>" % q for q in faq)) + cta_band()
    page("quy-trinh.html", "Quy trình làm việc và cam kết | Lộc Minh Anh",
         "Quy trình 5 bước của Lộc Minh Anh từ tiếp nhận, thiết kế, ký hợp đồng, thi công đến bàn giao, cùng cam kết về tiến độ, chất lượng và bảo hành.", main, active="quy-trinh.html")

# ---------------------------------------------------------------- TIN TỨC
def build_blog():
    cards = "".join('<a class="card rv" style="text-decoration:none;color:inherit;display:block" href="@/tin-tuc/%s.html"><span class="tag" style="margin:0 0 10px">%s · %s</span><h3>%s</h3><p>%s</p><span class="more" style="font-weight:600;color:var(--link)">Đọc bài viết →</span></a>'
                    % (p["slug"], p["tag"], p["read"], p["title"], esc(p["desc"])) for p in POSTS)
    main = hero_page("Tin tức và kiến thức xây dựng", "Những điều chủ nhà và chủ đầu tư nên biết trước khi xây dựng.", [HOME, "Tin tức"])
    main += '<section><div class="wrap"><h2 class="sr">Bài viết mới</h2><div class="grid g3">%s</div></div></section>' % cards + cta_band()
    page("tin-tuc.html", "Tin tức và kiến thức xây dựng | Lộc Minh Anh", "Bài viết hữu ích về báo giá xây nhà trọn gói, thủ tục xin phép xây dựng và cách chọn nhà thầu từ Lộc Minh Anh.", main, active="tin-tuc.html")
    for p in POSTS:
        art = json.dumps({"@context": "https://schema.org", "@type": "Article", "headline": p["title"], "description": p["desc"], "inLanguage": "vi",
                          "datePublished": TODAY, "dateModified": TODAY, "author": {"@type": "Organization", "name": "Lộc Minh Anh"},
                          "publisher": {"@type": "Organization", "name": "Lộc Minh Anh", "logo": {"@type": "ImageObject", "url": BASE + "assets/img/logo-lma.png"}},
                          "image": BASE + "assets/img/og-image.jpg", "mainEntityOfPage": BASE + "tin-tuc/%s.html" % p["slug"]}, ensure_ascii=False)
        m = hero_page(p["title"], '<time datetime="%s">19/10/2026</time> · %s · %s' % (TODAY, p["tag"], p["read"]), [HOME, '<a href="@/tin-tuc.html">Tin tức</a>', "Bài viết"])
        m += '<section><div class="wrap"><article class="article">%s<div class="btns"><a class="btn btn-gold" href="@/lien-he.html#bao-gia">Nhận tư vấn dự án</a><a class="btn btn-line" href="@/tin-tuc.html">← Bài viết khác</a></div></article></div></section>' % p["body"]
        page("tin-tuc/%s.html" % p["slug"], "%s | Lộc Minh Anh" % p["title"], p["desc"], m, active="tin-tuc.html", schema=art, og_type="article")

# ---------------------------------------------------------------- TUYỂN DỤNG
def build_jobs():
    main = hero_page("Tuyển dụng", "Cùng Lộc Minh Anh xây những công trình bền vững. Chúng tôi tìm người làm việc cẩn thận, có trách nhiệm và muốn phát triển nghề lâu dài.", [HOME, "Tuyển dụng"])
    main += ('<section><div class="wrap"><h2 class="sr">Môi trường làm việc</h2><div class="grid g3">'
             '<article class="card rv"><h3>An toàn là điều kiện đầu tiên</h3><p>Trang bị bảo hộ và quy định an toàn lao động được áp dụng tại mọi công trường.</p></article>'
             '<article class="card rv"><h3>Làm việc minh bạch</h3><p>Phân công rõ ràng, đánh giá theo kết quả công việc cụ thể.</p></article>'
             '<article class="card rv"><h3>Học hỏi từ thực tế</h3><p>Làm cùng đội ngũ có kinh nghiệm, trực tiếp tham gia công trình từ thiết kế đến bàn giao.</p></article></div></div></section>')
    main += ('<section class="alt"><div class="wrap"><div class="sec-head rv"><span class="kicker">Vị trí tuyển dụng</span><h2>Cơ hội làm việc</h2>'
             '<p class="note">Danh sách vị trí mẫu. Cập nhật theo nhu cầu thực tế, kèm mức thu nhập và địa điểm: %s.</p></div><div class="jobs">%s</div>'
             '<p style="margin-top:28px">Gửi hồ sơ và vị trí ứng tuyển về email <a href="@/lien-he.html" data-lma="email">[cập nhật]</a> hoặc liên hệ hotline <a href="@/lien-he.html" data-lma="hotline">[cập nhật]</a>.</p></div></section>'
             % (PH("cập nhật", ), "".join('<article class="card rv"><div style="display:flex;flex-wrap:wrap;justify-content:space-between;gap:12px;align-items:center"><div><h3>%s</h3><p style="margin:0">%s</p></div><a class="btn btn-line btn-sm" href="@/lien-he.html#bao-gia">Ứng tuyển</a></div></article>' % j for j in JOBS)))
    page("tuyen-dung.html", "Tuyển dụng | Lộc Minh Anh", "Cơ hội việc làm tại Lộc Minh Anh: chỉ huy trưởng, kỹ sư giám sát, dự toán, thiết kế kiến trúc – kết cấu. Gửi hồ sơ ứng tuyển.", main, active="tuyen-dung.html")

# ---------------------------------------------------------------- LIÊN HỆ
def build_contact():
    def li(ic, label, inner): return '<li><div class="ico">%s</div><div><b>%s</b>%s</div></li>' % (IC[ic], label, inner)
    info = "".join([
        li("pin", "Địa chỉ", '<span data-lma="address">[cập nhật]</span>'),
        li("phone", "Hotline", '<a href="@/lien-he.html" data-lma="hotline">[cập nhật]</a>'),
        li("chat", "Zalo", '<a href="@/lien-he.html" data-lma="zalo">Nhắn Zalo cho Lộc Minh Anh</a>'),
        li("mail", "Email", '<a href="@/lien-he.html" data-lma="email">[cập nhật]</a>'),
        li("clock", "Giờ làm việc", '<span data-lma="hours">[cập nhật]</span>'),
        li("fb", "Facebook", '<a href="@/lien-he.html" data-lma="facebook">Trang Facebook Lộc Minh Anh</a>')])
    form = """<form class="form" id="quote-form" novalidate>
<div class="row2"><div><label for="f-name">Họ và tên <span class="req" aria-hidden="true">*</span></label><input id="f-name" name="name" autocomplete="name" required aria-describedby="e-name"><p class="err" id="e-name" role="alert"></p></div>
<div><label for="f-phone">Số điện thoại <span class="req" aria-hidden="true">*</span></label><input id="f-phone" name="phone" type="tel" inputmode="tel" autocomplete="tel" placeholder="0905 123 456" required aria-describedby="e-phone"><p class="err" id="e-phone" role="alert"></p></div></div>
<div class="row2"><div><label for="f-type">Loại công trình <span class="req" aria-hidden="true">*</span></label><select id="f-type" name="type" required aria-describedby="e-type"><option value="">Chọn loại công trình</option><option>Nhà phố, biệt thự, nhà ở</option><option>Văn phòng, cửa hàng, thương mại</option><option>Nhà xưởng, kho, công nghiệp</option><option>Cải tạo, sửa chữa</option><option>Khác</option></select><p class="err" id="e-type" role="alert"></p></div>
<div><label for="f-area">Diện tích dự kiến (m²)</label><input id="f-area" name="area" type="number" inputmode="decimal" min="1" step="any" aria-describedby="e-area"><p class="err" id="e-area" role="alert"></p></div></div>
<div class="row2"><div><label for="f-loc">Địa điểm xây dựng</label><input id="f-loc" name="location" autocomplete="address-level2" placeholder="Quận/huyện, tỉnh/thành"></div>
<div><label for="f-budget">Ngân sách dự kiến</label><select id="f-budget" name="budget"><option value="">Chưa xác định</option><option>Dưới 1 tỷ đồng</option><option>1 – 3 tỷ đồng</option><option>3 – 5 tỷ đồng</option><option>Trên 5 tỷ đồng</option></select></div></div>
<div><label for="f-note">Ghi chú</label><textarea id="f-note" name="note" placeholder="Mô tả ngắn nhu cầu, tiến độ mong muốn, tình trạng bản vẽ..."></textarea></div>
<div class="hp" aria-hidden="true"><label>Không điền <input name="website" tabindex="-1" autocomplete="off"></label></div>
<div><label class="chk" for="f-consent"><input id="f-consent" name="consent" type="checkbox" aria-describedby="e-consent"><span>Tôi đồng ý để Lộc Minh Anh liên hệ qua điện thoại hoặc Zalo về yêu cầu này. <span class="req" aria-hidden="true">*</span></span></label><p class="err" id="e-consent" role="alert"></p></div>
<div id="form-msg" class="msg" role="status" tabindex="-1" hidden></div>
<button class="btn btn-gold" type="submit">Gửi yêu cầu báo giá</button></form>"""
    main = hero_page("Liên hệ và nhận báo giá", "Mô tả ngắn công trình của bạn. Lộc Minh Anh sẽ liên hệ để khảo sát và gửi báo giá chi tiết theo hạng mục.", [HOME, "Liên hệ"])
    main += ('<section><div class="wrap split"><div class="rv"><span class="kicker">Thông tin liên hệ</span><h2>Gặp trực tiếp hoặc gọi cho chúng tôi</h2><ul class="contact-list">%s</ul>'
             '<div class="map" id="map"><div class="ph"><span>Bản đồ nhúng: điền mapEmbed trong script.js</span></div></div></div>'
             '<div class="rv" id="bao-gia"><span class="kicker">Báo giá và tư vấn</span><h2>Gửi yêu cầu của bạn</h2>%s</div></div></section>' % (info, form))
    page("lien-he.html", "Liên hệ và nhận báo giá | Lộc Minh Anh", "Liên hệ Lộc Minh Anh để được tư vấn và báo giá tổng thầu xây dựng tại miền Trung. Gửi form hoặc gọi hotline, Zalo.", main, active="lien-he.html", schema=schema_org())

def build_404():
    page("404.html", "Không tìm thấy trang | Lộc Minh Anh", "Trang bạn tìm không tồn tại hoặc đã được chuyển.",
         '<section><div class="wrap center"><span class="kicker">Lỗi 404</span><h1>Không tìm thấy trang</h1><p class="lead">Trang bạn cần có thể đã được chuyển hoặc đường dẫn chưa đúng.</p><div class="btns" style="justify-content:center"><a class="btn btn-gold" href="@/index.html">Về trang chủ</a><a class="btn btn-line" href="@/lien-he.html">Liên hệ</a></div></div></section>')

def build_seo():
    urls = ["", "gioi-thieu.html", "dich-vu.html", "du-an.html", "quy-trinh.html", "tin-tuc.html", "tuyen-dung.html", "lien-he.html"] \
        + ["du-an/%s.html" % p["slug"] for p in PROJECTS] + ["tin-tuc/%s.html" % p["slug"] for p in POSTS]
    x = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    for u in urls:
        x += "  <url><loc>%s%s</loc><lastmod>%s</lastmod><priority>%s</priority></url>\n" % (BASE, u, TODAY, "1.0" if u == "" else "0.7")
    (ROOT / "sitemap.xml").write_text(x + "</urlset>\n", encoding="utf-8")
    (ROOT / "robots.txt").write_text("User-agent: *\nAllow: /\n\nSitemap: %ssitemap.xml\n" % BASE, encoding="utf-8")

if __name__ == "__main__":
    build_home(); build_about(); build_services(); build_projects(); build_process(); build_blog(); build_jobs(); build_contact(); build_404(); build_seo()
    print("Đã sinh", len(list(ROOT.rglob("*.html"))), "trang HTML")
