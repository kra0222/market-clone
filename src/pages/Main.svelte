<script>
  import { onMount } from "svelte";
  import Nav from "./components/ Nav.svelte";
  import { getDatabase, ref, onValue } from "firebase/database";

  const hour = new Date().getHours();
  const minute = new Date().getMinutes();

  $: items = []; //반응형 변수

  const calcTime = (timestamp) => {
    const curTime = new Date().getTime() - 9 * 60 * 60 * 1000;
    const time = new Date(curTime - timestamp);
    const hour = time.getHours();
    const minute = time.getMinutes();
    const second = time.getSeconds();

    if (hour > 0) return `${hour}시간 전`;
    else if (minute > 0) return `${minute}분 전`;
    else if (second > 0) return `${second}초 전`;
    else "방금 전";
  };

  const db = getDatabase();
  const itmesRef = ref(db, "items/");

  onMount(() => {
    //처음 랜더링 될 때 한 번만 실행되고 데이터를 가져오지 않음, 이럴 때 온마운트를 사용하여 랜더링 될 때마다 onValue가 호출될 수 있도록 함
    onValue(itmesRef, (snapshot) => {
      const data = snapshot.val();
      items = Object.values(data).reverse();
    });
  });
</script>

<header>
  <div class="info-bar">
    <div class="info-bar__time">{hour}:{minute}</div>
    <div class="info-bar__icons">
      <img src="assets/chart-bar.svg" alt="chart-bar" />
      <img src="assets/wifi.svg" alt="wifi" />
      <img src="assets/battery.svg" alt="battery" />
    </div>
  </div>
  <div class="menu-bar">
    <div class="menu-bar__location">
      <div>역삼1동</div>
      <div class="menu-bar__location-icon">
        <img src="assets/arrow.svg" alt="arrow" />
      </div>
    </div>
    <div class="menu-bar__icons">
      <img src="assets/search.svg" alt="search" />
      <img src="assets/bars.svg" alt="bars" />
      <img src="assets/bell.svg" alt="bell" />
    </div>
  </div>
</header>
<main>
  {#each items as item}
    <div class="item-list">
      <div class="item-list__img">
        <img alt={item.title} src={item.imgUrl} />
      </div>
      <div class="item-list__info">
        <div class="item-list__info-title">{item.title}</div>
        <div class="item-list__info-price">
          {item.price}
        </div>
        <div>{item.description}</div>
        <div class="item-list__info-meta">
          {item.place}
          {calcTime(item.insertAt)}
        </div>
      </div>
    </div>
  {/each}
  <div>
    <a class="write-btn" href="#/write">+ 글쓰기</a>
  </div>
</main>
<Nav location="home" />
<div class="media-info-msg">화면 사이즈를 줄여 주세요</div>
