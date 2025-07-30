<script>
  import { getDatabase, ref, push } from "firebase/database";
  import Nav from "./components/ Nav.svelte";
  import {
    getStorage,
    ref as refImage,
    uploadBytes,
    getDownloadURL,
  } from "firebase/storage";

  let title;
  let price;
  let description;
  let place;
  let files;

  const db = getDatabase();
  const storage = getStorage();

  function writeUserData(imgUrl) {
    push(ref(db, "items/"), {
      title,
      price,
      description,
      place,
      insertAt: new Date().getTime(),
      imgUrl,
    });
    alert("글쓰기 완료");
    window.location.hash = "/";
  }

  // 'file' comes from the Blob or File API
  // uploadBytes(storageRef, file).then((snapshot) => {
  //   console.log("Uploaded a blob or file!");
  // });

  // $: if (files) console.log(files); //files가 바뀔 때마다 찍힘

  //제출 버튼 -> 저장소에 업로드 -> url을 이용하여 가져오기
  //이미지를 firebase storage에 업로드함
  const uploadFile = async () => {
    const file = files[0];
    const name = file.name;
    const imgRef = refImage(storage, name);
    await uploadBytes(imgRef, file);
    const url = await getDownloadURL(imgRef); //url을 실시간 데이터베이스에 삽입하며 이미지도 같이 띄울 수 있도록 함
    return url;
  };

  const handleSubmit = async () => {
    const url = await uploadFile(); //url 정보를 받음
    writeUserData(url); //넘김
  };
</script>

<form id="write-form" on:submit|preventDefault={handleSubmit}>
  <div>
    <label for="image">이미지</label>
    <input type="file" bind:files id="image" name="image" />
  </div>
  <div>
    <label for="title">제목</label>
    <input type="text" id="title" name="title" bind:value={title} />
  </div>
  <div>
    <label for="price">가격</label>
    <input type="number" id="price" name="price" bind:value={price} />
  </div>
  <div>
    <label for="description">설명</label>
    <input
      type="text"
      id="description"
      name="description"
      bind:value={description}
    />
  </div>
  <div>
    <label for="place">장소</label>
    <input type="text" id="place" name="place" bind:value={place} />
  </div>
  <div>
    <button class="write-button" type="submit">제출</button>
  </div>
</form>
<Nav location="write" />

<style>
  .write-button {
    border: none;
    margin: 9px 50px;
    padding: 5px 10px;
    border-radius: 9px;
    cursor: pointer;
    background-color: salmon;
    color: white;
    width: 70px;
    height: 30px;
    text-align: center;
  }
</style>
