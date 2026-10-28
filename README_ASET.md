# Fairy Quest: Menjemput Tim — Paket Aset

Aset untuk micro game GDevelop 2D (top-down, pixel art). Semua gambar dibuat **1 piksel = 1 piksel** (tanpa blur), jadi harus diperbesar dengan mode *nearest*.

## 1. Pengaturan proyek GDevelop (penting)
- **Resolusi game: 640 × 360** (semua ukuran UI di paket ini dirancang untuk ini; tampil 2× di 1280×720, 3× di 1920×1080).
- Di *Project properties*, set **scale mode / sampling ke "Nearest"** (tanpa antialiasing, untuk pixel art) dan aktifkan **pixel rounding** kalau ada. Nama opsi bisa sedikit beda antar versi.
- Pilih "Adapt game resolution to window size" / mode skala yang menjaga rasio, supaya gambar tetap tajam.
- Font: pakai `fonts/PressStart2P-Regular.ttf` (lisensi OFL, boleh dipakai gratis). **Ukuran teks 8** (atau kelipatan 8: 16, 24) supaya tajam.

## 2. Isi folder
```
sprites/player/    peri: jalan 4 arah x 4 frame (strip + frames/), idle 4 arah, sheet 4 arah
sprites/npc/       3 teman: idle (2 frame) & wave (2 frame)  -> template, bisa kalian edit
sprites/enemy/     shadow_wisp (rintangan bergerak, 2 frame)
items/             serbuk bintang, bintang emas, embun, jamur, buah + efek (sparkle, burst, firefly)
mission/           bunga cahaya, lentera, kristal (3 warna, mati/nyala), lencana 1-3,
                   kabut penghalang, semak duri, panah penunjuk, bantalan checkpoint
tiles/             tile 32x32 (grass, path, water, swamp, crystal floor, dll) + tileset gabungan
decor/             pohon, semak, batu, jamur, alang-alang, teratai, papan pos 1-3, gerbang START,
                   bendera FINISH, Pohon Cahaya (redup & menyala)
ui/                panel 9-patch, bingkai potret, nameplate, tombol (3 state), HUD, ikon, banner, logo
portraits/         potret SEMENTARA 64x64 (ganti dengan foto pixel art teman, lihat bagian 5)
backgrounds/       bg_menu & bg_ending 640x360
audio/music/       5 musik loop (.ogg)     audio/music_wav_loopmulus/  versi .wav (loop paling mulus)
audio/sfx/         17 efek suara (.wav)
tools/             pixelate_foto.py  (ubah foto jadi pixel art)
previews/          gambar contoh tampilan + katalog semua aset
```
File animasi ada dua bentuk: `nama_strip.png` (semua frame berjajar horizontal) dan `frames/nama_0.png, nama_1.png, ...` (per frame). Untuk GDevelop paling gampang: di editor Sprite, *Add a sprite → pilih semua file di folder `frames/`* untuk animasi tersebut.

## 3. Pemetaan aset → objek GDevelop
| Objek | Aset | Animasi / catatan |
|---|---|---|
| `Peri` (Sprite) | `player_walk_down/left/right/up` | 4 animasi jalan, kecepatan ±0.12 dtk/frame. Idle = frame 0. Behavior: **Top-down movement**. Collision mask kecil di badan (±12×14 px), bukan sayap |
| `Teman1/2/3` (Sprite) | `friend1/2/3_idle`, `_wave` | idle 0.5 dtk/frame; wave saat Peri dekat |
| `Seru` | `ui_icon_exclaim` | muncul di atas teman saat Peri mendekat |
| `Bintang` | `item_star_dust` | variabel objek `nilai = 5` |
| `BintangEmas` | `item_star_gold` | `nilai = 50` |
| `Embun`, `Jamur`, `Buah` | `item_dew_drop`, `item_speed_mushroom`, `item_light_fruit` | efek: waktu +5 dtk / kecepatan / +25 skor |
| `BungaCahaya` | `mission_flower_light` | misi pos 1 |
| `Lentera` | `mission_lantern` | misi pos 2 |
| `Kristal1/2/3` | `mission_crystal_*_off` / `_on` | ganti ke `_on` saat disentuh (misi pos 3) |
| `Lencana1/2/3` | `mission_badge_1/2/3` + `ui_badge_slot_empty` | tampil di HUD setelah misi selesai |
| `Kabut` | `obstacle_fog_barrier` | penghalang jalan; hapus saat misi selesai (+ `sfx_gate_open`) |
| `Duri` | `obstacle_thorn_bush` | sentuh = −10 skor + `sfx_hit_obstacle` |
| `Bayangan` | `shadow_wisp` | musuh patroli, efeknya sama dengan duri |
| `Rumput/Jalan/Air` | `tile_*` | pakai objek **Tiled Sprite** ukuran bebas; air animasi: `tile_water` (2 frame) |
| `Start`, `Pos1-3`, `Finish` | `decor_start_gate`, `decor_sign_pos1..3`, `decor_flag_finish`, `marker_checkpoint_pad` | |
| `PohonCahaya` | `decor_tree_of_light_dim` → `_lit` | ganti ke `_lit` saat 3 lencana terkumpul |
| Pohon & dekor | `decor_tree_green/autumn/swamp`, dll. | atur **Z-order = Y** supaya Peri bisa lewat di depan/belakang pohon |

Saran tema per area: Pos 1 `tile_grass_flowers` + pohon hijau, Pos 2 `tile_water` + teratai + alang-alang, Pos 3 `tile_swamp`/`tile_crystal_floor` + pohon rawa, Finish dengan `tile_grass_a` + Pohon Cahaya.

## 4. Pop-up profil (sesuai contoh referensi)
Susunan pada resolusi 640×360 (lihat `previews/preview_profile_popup_640x360.png`):
- **Kotak dialog:** objek **Panel Sprite (9-patch)** dari `ui_panel_9patch_margin8.png`, **margin 8 di keempat sisi**, ukuran 520×84 di posisi (104, 262).
- **Potret:** gambar potret 64×64 di (26, 246), lalu **`ui_portrait_frame_76.png` di atasnya** di (20, 240).
- **Nama plat:** `ui_nameplate_76x16.png` di (20, 320) dengan teks "TEMAN 1".
- **Teks:** 3 objek Text ukuran 8: Nama, NIM, Hobi (contoh warna: putih / kuning `#FFE45E` / hijau `#86E098`).
- **Tombol NEXT:** sprite `ui_button_next_64` (3 frame: normal, hover, pressed), dan `ui_icon_next_arrow` (2 frame) kalau mau panah berkedip.
- Semua elemen pop-up dimasukkan ke satu **grup objek** supaya mudah ditampilkan/disembunyikan; kalau mau, redupkan layar dengan persegi hitam transparan 35% di belakangnya.
- Saat tombol NEXT diklik: sembunyikan pop-up, set `misiAktif`, tampilkan `ui_banner_misi_baru` sebentar, lalu panel misi di HUD.

HUD: `ui_hud_score_96x24` (teks skor ditaruh di kanan bintang), `ui_hud_timer_72x24`, 3 slot lencana, panel misi 9-patch (`ui_panel_9patch_margin8` atau versi krem). Layar akhir: `ui_banner_misi_selesai`, `ui_rating_star_full/empty`, `ui_button_main_lagi_120`. Layar menu: `bg_menu`, `ui_title_logo_280x84`, `ui_button_mulai_96`.

## 5. Foto pixel art teman-teman (WAJIB DIGANTI)
`portraits/portrait_placeholder_friend1..3_64.png` hanyalah **pengganti sementara**. Buat potret asli dari foto wajah kalian:

```
pip install pillow
python tools/pixelate_foto.py foto_teman1.jpg --name friend1
python tools/pixelate_foto.py foto_teman2.jpg --name friend2 --zoom 1.3
python tools/pixelate_foto.py foto_teman3.jpg --name friend3 --crop 120,60,400,400
```
Hasil di folder `hasil_pixel/portrait_friendN_64.png` (kotak 64×64, cocok untuk bingkai). Opsi yang berguna:
- `--grid 24` (lebih kasar/blocky) atau `--grid 48 --size 96` (lebih detail, bingkai harus diperbesar).
- `--colors 12` mengurangi warna supaya terlihat lebih "pixel art".
- `--zoom 1.3` memperbesar wajah, `--shift-y -0.2` menggeser area ke atas, `--crop x,y,lebar,tinggi` untuk crop manual.
Pakai foto yang wajahnya jelas dan menghadap depan. Foto asli tidak perlu dikumpulkan di repo — cukup hasil pixel-nya.

Sprite teman (`friendN_*`) juga masih **template generik** (topi, rambut panjang, kacamata). Edit warna rambut, baju, dan aksesorinya di Aseprite/Piskel/LibreSprite supaya mirip masing-masing orang.

## 6. Musik & efek suara
| Kapan | File |
|---|---|
| Menu | `bgm_01_menu` |
| Pos 1 (pagi) | `bgm_02_pos1_pagi` |
| Pos 2 (sore) | `bgm_03_pos2_sore` |
| Misi pos 3 (berwaktu) | `bgm_04_pos3_misi` |
| Finish / ending | `bgm_05_finish_ending` |

Setel musik **loop**, volume 40–60%. Saat pindah area, hentikan musik lama baru putar yang baru. Kalau terdengar jeda di titik loop saat memakai `.ogg`, pakai versi `.wav` di `music_wav_loopmulus/`.

| Kejadian | SFX |
|---|---|
| Ambil serbuk bintang / bintang emas | `sfx_pickup_star` / `sfx_pickup_star_gold` |
| Embun / jamur / buah | `sfx_pickup_dew` / `sfx_powerup_mushroom` / `sfx_pickup_fruit` |
| Kena duri / bayangan | `sfx_hit_obstacle` |
| Pop-up profil muncul | `sfx_popup_profile` |
| Klik NEXT | `sfx_click_next` |
| Misi dimulai / selesai | `sfx_mission_accept` / `sfx_mission_complete` |
| Dapat lencana | `sfx_badge_get` |
| Kabut/gerbang terbuka | `sfx_gate_open` |
| Timer (tiap detik / 10 detik terakhir) | `sfx_timer_tick` / `sfx_timer_warning` |
| Waktu habis | `sfx_game_over_time_up` |
| Menang | `sfx_win_fanfare`, lalu `sfx_star_rating` per bintang rating |

Musik dan SFX dihasilkan lewat sintesis chiptune (bukan rekaman), jadi tidak memakai karya orang lain. Kalau kurang cocok di telinga, ganti dengan musik bebas lisensi (OpenGameArt, Pixabay Music, itch.io CC0) dan cantumkan kredit.

## 7. Lisensi & kredit
- Gambar, animasi, musik, dan SFX: dibuat khusus untuk proyek ini, bebas dipakai untuk tugas kelompok kalian.
- Font Press Start 2P © The Press Start 2P Project Authors, lisensi SIL OFL 1.1 (`fonts/OFL.txt`). Cantumkan di layar kredit: "Font: Press Start 2P (OFL)".
- Karakter peri adalah desain orisinal (bukan karakter berhak cipta); nama bisa kalian ganti sesuka hati.
