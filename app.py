import streamlit as st # pip install streamlit==0.82.0
import requests
import os
import base64
from  PIL import Image
from streamlit_option_menu import option_menu
import streamlit.components.v1 as html


###logo###
image = Image.open('gadang2-.png')

# membuat container untuk menampilkan gambar dan garis
container = st.container()

# menampilkan gambar di dalam container
with container:
    col1, col2, col3 = st.columns([1, 1, 1]) # membuat 3 kolom, dengan kolom tengah lebih lebar
    
    with col2:
        st.image(
            image,
            use_column_width=True, # mengatur lebar gambar sama dengan lebar kolom
            output_format='auto' # menyesuaikan format gambar secara otomatis
           
        )
    
    container_width = container.width
    col1.header("") # mengisi kolom 1 dengan header kosong agar kolom 2 berada di tengah
    col3.header("") # mengisi kolom 3 dengan header kosong agar kolom 2 berada di tengah
    
    # menambahkan styling pada wadah gambar menggunakan markdown
    st.markdown(
        f"<div style='text-align: center; width: {container_width}px;'>"
        f"</div>",
        unsafe_allow_html=True
    )

####logo###



def add_bg_from_local(image_file):
    with open(image_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    st.markdown(
    f"""
    <style>
.stApp {{background-image: url(data:image/{"png"};base64,{encoded_string.decode()});
        background-size: cover
    }}
    </style>
    """,
    unsafe_allow_html=True
    )
add_bg_from_local('bunda.png')     

def get_data(url):
	resp = requests.get(url)
	return resp.json()


#sidebar
with st.sidebar:
    choose = option_menu("Galeri Aplikasi", ["Translasi", "Tentang" ],
                         icons=['translate', 'book','house'],
                         menu_icon="app-indicator", default_index=0,
                         styles={
        "container": {"padding": "5!important", "background-color": "#fafafa"},
        "icon": {"color": "#C21616", "font-size": "25px"}, 
        "nav-link": {"font-size": "16px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
        "nav-link-selected": {"background-color": "#FFB90F"},
    }
    )



if choose == "Tentang":
    col1, col2 = st.columns( [100, 0.2])
    with col1:               # To display the header text using css style
        st.markdown(""" <style> .font {
        font-size:35px ; font-family: 'Cooper Black'; color: #C21616; text-align: center;} 
        </style> """, unsafe_allow_html=True)
        st.markdown('<p class="font">TENTANG KAMI</p>', unsafe_allow_html=True)    
        st.markdown('<style>body {background-color: #f5f5f5;} p {font-size:20px ;} p {text-align: justify;}</style>', unsafe_allow_html=True)
        kalimat = "Assalamualaikum! Translasi Bahasa Minangkabau merupakan kamus bahasa Minangkabau. aplikasi ini dapat melakukan terjemahan bahasa Minangkabau ke bahasa indonesia atau bahasa indonesia ke bahasa Minangkabau secara online. Anda dapat mempelajari kata dan kosakata yang ada di dalam bahasa Minangkabau secara online. Kami juga menyediakan aksara Lampung untuk dipelajari. Aplikasi ini dapat menjadi referensi anda dalam belajar bahasa Minangkabau. Mari kita lestarikan budaya Minangkabau dengan tetap belajar dan mengetahui bahasa Minangkabau."
        st.markdown(kalimat, unsafe_allow_html=True)


        

elif choose == "Translasi":
    col1, col2 = st.columns( [100, 0.2])
    with col1:               # To display the header text using css style

        st.markdown(""" <style> .font {
        font-size:35px ;  font-family: 'Cooper Black'; color: #C21616;   transform: translateX(8%); text-align: justify;} 
        </style> """, unsafe_allow_html=True)
        st.markdown('<p class="font">Translasi Bahasa Minangkabau</p>', unsafe_allow_html=True)    
    base_url = "https://bade.jasaedukasi.com/translator?versi=2&mode={}&bahasa={}&text={}"

    Languages = {'Minangkabau':'padang_minang','Indonesia':'indonesia'}

            

    with st.form(key="search form"):

        search_term = st.text_area("Masukan teks anda disini")
        # text = st.text_area("Enter text:",height=None,max_chars=None,key=None,help="Enter your text here")

        option1 = st.radio('Bahasa asal', ('Minangkabau', 'Indonesia'))
        option2 = st.radio('Bahasa tujuan', ('Minangkabau', 'Indonesia'))

        value1 = Languages[option1]
        value2 = Languages[option2]
        
    
        submit_search =  st.form_submit_button(label='Translasi')
        if submit_search:
            if search_term == "":
                st.error('Mohon masukan teks untuk translasi')
            elif value1 == value2:
                st.error('Tidak bisa mentranslasi bahasa yang sama')
               
            elif value1 == "padang_minang":
                mode = 1
                # Create Search Query
                search_url = base_url.format(mode, value1, search_term)
                # st.write(search_url)
                data = get_data(search_url)
                # st.success(data)
                resultfinal = ""
                for i in range(len(data['response']['indonesia'])):
                    result = data['response']['indonesia'][i]['k']
                    resultfinal = resultfinal + " " + result
                    # st.success(resultfinal)
                st.markdown(
                    f"<div class='st-alert st-alert-success' style='background-color: #ffffb0; font-size: 20px; font-weight: bold;'>Dalam Bahasa {option2} artinya: {resultfinal}</div>",
                    unsafe_allow_html=True,
                )


            
            elif value1 == "indonesia":
                mode = 2
                # Create Search Query
                search_url = base_url.format(mode, value2, search_term)
                # st.write(search_url)
                data = get_data(search_url)
                # st.success(data)
                resultfinal = ""
                for i in range(len(data['response']['daerah'])):
                    # st.write(i)
                    result = data['response']['daerah'][i]['k']
                    resultfinal = resultfinal + " " + result
                    
                # st.success(resultfinal)
                st.markdown(
                    f"<div class='st-alert st-alert-success' style='background-color: #ffffb0; font-size: 20px; font-weight: bold;'>Dalam Bahasa {option2} artinya: {resultfinal}</div>",
                    unsafe_allow_html=True,
                )
                # translate = translator.translate(text,lang_src=value1,lang_tgt=value2)
                # st.info(str(translate))
                
                