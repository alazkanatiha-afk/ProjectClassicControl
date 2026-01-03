from flask import Flask, render_template_string

app = Flask(__name__)

# ProjectClassicControl - Standalone Single-File Version
# All HTML, CSS, and JS are embedded within this single Python script for easy sharing.

HTML_CONTENT = """
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ProjectClassicControl - UAV Kontrol Sistemi</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: linear-gradient(135deg, #0a0e27 0%, #1a1f3a 100%); color: #e0e0e0; line-height: 1.6; transition: background 0.3s, color 0.3s; }
        body.light-mode { background: linear-gradient(135deg, #f0f4f8 0%, #d9e2ec 100%); color: #1a202c; }
        .demo-banner { background: linear-gradient(90deg, #ff6b35 0%, #f7931e 100%); color: #fff; text-align: center; padding: 12px 20px; font-weight: 600; font-size: 14px; box-shadow: 0 2px 10px rgba(255, 107, 53, 0.3); }
        body.light-mode .demo-banner { background: linear-gradient(90deg, #ff8a50 0%, #ffa94d 100%); }
        header { background: rgba(10, 14, 39, 0.95); backdrop-filter: blur(10px); padding: 20px 0; position: sticky; top: 0; z-index: 1000; border-bottom: 1px solid rgba(0, 174, 255, 0.2); }
        body.light-mode header { background: rgba(255, 255, 255, 0.95); border-bottom: 1px solid rgba(0, 174, 255, 0.3); }
        nav { max-width: 1200px; margin: 0 auto; display: flex; justify-content: space-between; align-items: center; padding: 0 30px; }
        .logo { font-size: 24px; font-weight: bold; color: #00aeff; text-decoration: none; display: flex; align-items: center; gap: 10px; }
        .logo::before { content: "✈"; font-size: 28px; }
        body.light-mode .logo { color: #0077cc; }
        .theme-toggle { background: rgba(0, 174, 255, 0.2); border: 2px solid #00aeff; color: #00aeff; padding: 8px 16px; border-radius: 25px; cursor: pointer; font-weight: 600; transition: all 0.3s; font-size: 14px; }
        .theme-toggle:hover { background: #00aeff; color: #fff; transform: scale(1.05); }
        body.light-mode .theme-toggle { background: rgba(0, 119, 204, 0.1); border: 2px solid #0077cc; color: #0077cc; }
        nav ul { list-style: none; display: flex; gap: 30px; }
        nav a { color: #e0e0e0; text-decoration: none; transition: color 0.3s; font-weight: 500; }
        nav a:hover { color: #00aeff; }
        body.light-mode nav a { color: #2d3748; }
        .container { max-width: 1200px; margin: 0 auto; padding: 60px 30px; }
        .hero { text-align: center; padding: 80px 30px; background: linear-gradient(135deg, rgba(0, 174, 255, 0.1) 0%, rgba(72, 202, 228, 0.1) 100%); border-radius: 20px; margin-bottom: 60px; }
        body.light-mode .hero { background: linear-gradient(135deg, rgba(0, 174, 255, 0.15) 0%, rgba(72, 202, 228, 0.15) 100%); }
        .hero h1 { font-size: 48px; color: #00aeff; margin-bottom: 20px; text-shadow: 0 0 20px rgba(0, 174, 255, 0.5); }
        body.light-mode .hero h1 { color: #0077cc; text-shadow: 0 0 20px rgba(0, 119, 204, 0.3); }
        .hero p { font-size: 20px; color: #b0b0b0; max-width: 700px; margin: 0 auto 30px; }
        body.light-mode .hero p { color: #4a5568; }
        .cta-button { display: inline-block; background: linear-gradient(135deg, #00aeff 0%, #48cae4 100%); color: #fff; padding: 15px 40px; border-radius: 50px; text-decoration: none; font-weight: 600; transition: transform 0.3s, box-shadow 0.3s; box-shadow: 0 5px 20px rgba(0, 174, 255, 0.4); }
        .cta-button:hover { transform: translateY(-3px); box-shadow: 0 8px 30px rgba(0, 174, 255, 0.6); }
        section { margin-bottom: 80px; }
        h2 { font-size: 36px; color: #00aeff; margin-bottom: 30px; text-align: center; }
        body.light-mode h2 { color: #0077cc; }
        .section-content { background: rgba(26, 31, 58, 0.6); padding: 40px; border-radius: 15px; border: 1px solid rgba(0, 174, 255, 0.2); }
        body.light-mode .section-content { background: rgba(255, 255, 255, 0.8); border: 1px solid rgba(0, 174, 255, 0.3); color: #2d3748; }
        .features-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 30px; margin-top: 40px; }
        .feature-card { background: rgba(26, 31, 58, 0.8); padding: 30px; border-radius: 15px; border: 1px solid rgba(0, 174, 255, 0.2); transition: transform 0.3s, border-color 0.3s; }
        body.light-mode .feature-card { background: rgba(255, 255, 255, 0.9); border: 1px solid rgba(0, 174, 255, 0.3); }
        .feature-card:hover { transform: translateY(-5px); border-color: #00aeff; }
        .feature-icon { font-size: 40px; margin-bottom: 15px; }
        .feature-card h3 { color: #48cae4; margin-bottom: 15px; font-size: 22px; }
        body.light-mode .feature-card h3 { color: #0077cc; }
        .feature-card p { color: #b0b0b0; line-height: 1.7; }
        body.light-mode .feature-card p { color: #4a5568; }
        .timeline { position: relative; padding-left: 40px; }
        .timeline-item { background: rgba(26, 31, 58, 0.8); padding: 25px; border-radius: 10px; margin-bottom: 25px; border-left: 4px solid #00aeff; position: relative; }
        body.light-mode .timeline-item { background: rgba(255, 255, 255, 0.9); border-left: 4px solid #0077cc; }
        .timeline-item::before { content: "◆"; position: absolute; left: -28px; top: 25px; color: #00aeff; font-size: 20px; }
        .timeline-item h3 { color: #48cae4; margin-bottom: 10px; }
        body.light-mode .timeline-item h3 { color: #0077cc; }
        .timeline-item p { color: #b0b0b0; }
        body.light-mode .timeline-item p { color: #4a5568; }
        footer { background: rgba(10, 14, 39, 0.95); padding: 40px 30px; text-align: center; border-top: 1px solid rgba(0, 174, 255, 0.2); }
        body.light-mode footer { background: rgba(255, 255, 255, 0.95); border-top: 1px solid rgba(0, 174, 255, 0.3); }
        footer p { color: #b0b0b0; margin-bottom: 10px; }
        body.light-mode footer p { color: #4a5568; }
        .social-links { margin-top: 20px; }
        .social-links a { color: #00aeff; text-decoration: none; margin: 0 15px; font-size: 18px; transition: color 0.3s; }
        @media (max-width: 768px) { nav ul { display: none; } .hero h1 { font-size: 32px; } }
        @keyframes float { 0%%, 100%% { transform: translateY(0px); } 50%% { transform: translateY(-20px); } }
        .tech-icon { animation: float 3s ease-in-out infinite; }
    </style>
</head>
<body>
    <div class="demo-banner">⚠️ Bu proje şu anda DEMO aşamasındadır. Aktif geliştirme devam ediyor!</div>
    <header>
        <nav>
            <a href="#home" class="logo">ProjectClassicControl</a>
            <div style="display: flex; align-items: center; gap: 30px;">
                <ul>
                    <li><a href="#home">Ana Sayfa</a></li>
                    <li><a href="#about">Hakkında</a></li>
                    <li><a href="#features">Özellikler</a></li>
                    <li><a href="#future">Gelecek Planları</a></li>
                </ul>
                <button class="theme-toggle" id="themeToggle">☀️ Gündüz</button>
            </div>
        </nav>
    </header>
    <div class="container">
        <div class="hero" id="home">
            <h1 class="tech-icon">ProjectClassicControl</h1>
            <p>Python tabanlı, modüler ve geliştirilmeye açık UAV (İnsansız Hava Aracı) kontrol sistemi. Drone'larınızı programatik olarak kontrol edin, otonom uçuş senaryoları oluşturun.</p>
            <a href="#features" class="cta-button">Özellikleri Keşfet →</a>
        </div>
        <section id="about">
            <h2>Proje Hakkında</h2>
            <div class="section-content">
                <p><strong>UAV Kontrol Sistemi Nedir?</strong></p>
                <p>UAV kontrol sistemleri, drone'ların uçuş parametrelerini, sensör verilerini ve otonom davranışlarını yöneten yazılımlardır.</p>
                <br>
                <p><strong>ProjectClassicControl'ün Amacı</strong></p>
                <p>Bu proje, eğitim ve geliştirme amaçlı, açık kaynaklı bir UAV kontrol altyapısı sunmayı hedefler. Python'un sadeliği sayesinde başlangıç için idealdir.</p>
            </div>
        </section>
        <section id="features">
            <h2>Özellikler</h2>
            <div class="features-grid">
                <div class="feature-card">
                    <div class="feature-icon">🐍</div>
                    <h3>Python Tabanlı</h3>
                    <p>Kolay okunabilir ve geliştirilebilir Python kodu. Hızlı prototipleme desteği.</p>
                </div>
                <div class="feature-card">
                    <div class="feature-icon">🔧</div>
                    <h3>Modüler Yapı</h3>
                    <p>Her bileşen bağımsız modüller halinde organize edilmiş.</p>
                </div>
                <div class="feature-card">
                    <div class="feature-icon">📡</div>
                    <h3>Gerçek Zamanlı Kontrol</h3>
                    <p>Drone ile anlık iletişim ve sensör verilerini okuma.</p>
                </div>
            </div>
        </section>
        <section id="future">
            <h2>Gelecek Planları</h2>
            <div class="timeline">
                <div class="timeline-item">
                    <h3>🌐 JavaScript Tabanlı Web Arayüzü</h3>
                    <p>Modern web teknolojileri ile kullanıcı dostu kontrol paneli.</p>
                </div>
                <div class="timeline-item">
                    <h3>📱 Canlı Kontrol Paneli</h3>
                    <p>Tarayıcı üzerinden gerçek zamanlı drone kontrolü.</p>
                </div>
            </div>
        </section>
    </div>
    <footer>
        <p><strong>ProjectClassicControl</strong> - UAV Kontrol Sistemi</p>
        <div class="social-links">
            <a href="https://github.com">GitHub</a>
            <a href="mailto:alazkanatiha@gmail.com">İletişim</a>
        </div>
    </footer>
    <script>
        const themeToggle = document.getElementById('themeToggle');
        const body = document.body;
        themeToggle.addEventListener('click', () => {
            body.classList.toggle('light-mode');
            themeToggle.innerHTML = body.classList.contains('light-mode') ? '🌙 Gece' : '☀️ Gündüz';
        });
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function (e) {
                e.preventDefault();
                document.querySelector(this.getAttribute('href')).scrollIntoView({ behavior: 'smooth' });
            });
        });
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_CONTENT)

if __name__ == '__main__':
    print("ProjectClassicControl sunucusu baslatiliyor...")
    print("Adres: http://127.0.0.1:5000")
    app.run(debug=True)
