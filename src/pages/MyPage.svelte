<script>
  import { user$ } from "../store";
  import Nav from "./components/ Nav.svelte";

  const logout = () => {
    //유저정보와 로컬스토리지를 비워주면 됨
    user$.set(null);
    localStorage.removeItem("token");
  };
</script>

<div>나의 당근</div>
<button on:click={logout}>로그아웃</button>
<Nav location="my" />

<style>
  button {
    cursor: pointer;
    border: 1px solid rgba(0, 0, 0, 0.3);
    font-size: large;
  }
</style>
