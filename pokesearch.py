import re
from datetime import datetime

def parse(text):
    # 不要な部分を削除
    text = re.sub(r"これらはあなただけに表示されています • これらのメッセージを削除する", "", text)
    text = re.sub(r"Master’s Go Community", "", text)
    text = re.sub(r"BOT", "", text)
    text = re.sub(r" — 今日 \d+:\d+", "", text)
    text = re.sub(r"Found these .* with IVs .*", "", text)

    ##行ごとに分割
    sections = text.strip().split(':1_::2_::3_: :4_: :5_::6_::7_::8_:\n')

    pokemon_data = []

    for section in reversed(sections):
        if(not section.strip()):continue
        print(section)
        # 分割した後に各要素をstrip()してから読み取り
        lines = section.split("\n")
        print(lines)

        # ポケモン名、属性、光るかどうか、性別を取得
        name_info = re.split(r'\s*:\s*', lines[0][1:])
        name = name_info[0]
        can_be_shiny = 'shiny' in name_info
        gender = 'male' if 'male' in name_info else 'female' if 'female' in name_info else None

        # IV, CP, LVを取得
        iv_match = re.search(r':IV:\s*(\d+/\d+/\d+)', lines[1])
        cp_match = re.search(r':CP:\s*(\d+)', lines[1])
        lv_match = re.search(r':LV:\s*(\d+)', lines[1])

        iv = list(map(int, iv_match.group(1).split('/'))) if iv_match else None
        cp = int(cp_match.group(1)) if cp_match else None
        lv = int(lv_match.group(1)) if lv_match else None

        # Desapareceの情報を取得
        despawn_match = re.search(r'Desaparece: (.+)', lines[2])
        despawn_str = despawn_match.group(1) if despawn_match else None
        despawn = datetime.strptime(despawn_str, '%Y年%m月%d日 %H:%M') if despawn_str else None

        # ロケーション情報を取得
        location = lines[3][2:]

        # 座標情報を取得
        coord_raw = lines[4]
        lat, lon = map(float, coord_raw.split(','))

        # 結果を辞書にまとめる
        pokemon_info = {
            "name": name,
            "can_be_shiny": can_be_shiny,
            "gender": gender,
            "iv": iv,
            "cp": cp,
            "lv": lv,
            "despawn": despawn,
            "location": location,
            "coord": {"raw": coord_raw, "lat": lat, "lon": lon}
        }

        pokemon_data.append(pokemon_info)

    return pokemon_data
