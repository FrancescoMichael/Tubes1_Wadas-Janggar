# Pemanfaatan Algoritma Greedy dalam pembuatan bot permainan Diamonds

> Tugas Besar IF2211 Strategi Algoritma Kelas 1 Kelompok Wadas Janggar
> 
> Oleh Kelompok Algeo Lens:<br>
> 1. 13522020 Aurelius Justin Philo Fanjaya<br>
> 2. 13522038 Francesco Michael Kusuma<br>
> 3. 13522061 Maximilian Sulistiyo<br>
> 
> Sekolah Teknik Elektro dan Informatika<br>
> Institut Teknologi Bandung<br>
> Semester IV Tahun 2023/2024


## Table of Contents
* [General Info](#cara-kerja-algoritma)
* [Setup](#setup)
* [Usage](#usage)
* [Links](#links)


## Cara Kerja Algoritma
Backbone dari algoritma ini adalah dengan strategi Greedy. Terdapat berbagai cara pengimplementasian algoritma ini namun kita memilih untuk menggunakan _Greedy by Distance and Priority with Conditional Heuristics_ dimana kita pada dasarnya mementingkan jarak namun dalam hal itu juga mempertimbangkan beberapa hal yang di prioritaskan seperti kembali ke base jika kantong sudah penuh dan juga menyerang musuh jika jarak sudah dekat. Dengan itu kami berharap bahwa saat mengambil keputusan terbaik pada waktu itu kita dapat mencapai keuntungan maksimum pada skala global.

## Setup

Silahkan mengunduh python pada [link ini](https://www.python.org/downloads/). Kemudian dibutuhkan juga game engine pada [link ini](https://github.com/haziqam/tubes1-IF2211-game-engine/releases/tag/v1.1.0) dan juga starter pack bot yang bisa didapatkan pada [link ini](https://github.com/haziqam/tubes1-IF2211-bot-starter-pack/releases/tag/v1.0.1), untuk tutorial pemasangan game engine dan juga penjalanan starter pack bot dapat dilihat pada [link ini](https://docs.google.com/document/d/1L92Axb89yIkom0b24D350Z1QAr8rujvHof7-kXRAp7c/edit).

## Usage

Untuk menjalankan bot kita pada project ini cukup ketikkan ini pada shell

Untuk Windows
```shell
start cmd /c "python main.py --logic Greedy --email=janggar@email.com --name=Wadas --password=123456 --team etimo"
```

Untuk Linux dan MacOS
```shell
python3 main.py --logic Greedy --email=janggar@email.com --name=Wadas --password=123456 --team etimo &
```

## Links
- [Spesifikasi Tugas Besar 1 IF2211 Strategi Algoritma Semester II tahun 2023/2024](https://docs.google.com/document/d/13cbmMVXviyu8eKQ6heqgDzt4JNNMeAZO/edit).
- [This Repository](https://github.com/FrancescoMichael/Tubes1_Wadas-Janggar)
- [Laporan](https://docs.google.com/document/d/1bSYNi0zlVor9MehvM3DFhBvhNNDHoutrBIRpKqBsTAk/edit)