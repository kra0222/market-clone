<script>
  import Main from "./pages/Main.svelte";
  import Login from "./pages/Login.svelte";
  import Loding from "./pages/Loding.svelte";
  import Signup from "./pages/Signup.svelte";
  import Write from "./pages/Write.svelte";
  import MyPage from "./pages/MyPage.svelte";
  import Router from "svelte-spa-router";
  import NotFound from "./pages/NotFound.svelte";
  import "./css/style.css";
  import { user$ } from "./store";
  import {
    getAuth,
    GoogleAuthProvider,
    signInWithCredential,
  } from "firebase/auth";
  import { onMount } from "svelte";

  let isLoding = true; //처음 화면이 갔을 때는 로딩화면

  const auth = getAuth();

  const checkLogin = async () => {
    const token = localStorage.getItem("token");
    if (!token) return (isLoding = false);

    const credential = GoogleAuthProvider.credential(null, token);
    const result = await signInWithCredential(auth, credential);
    const user = result.user;
    user$.set(user);
    isLoding = false;
  };

  const routes = {
    "/": Main,
    "/signup": Signup,
    "/write": Write,
    "/my": MyPage,
    "*": NotFound,
  };

  onMount(() => checkLogin());
</script>

{#if isLoding}
  <Loding />
{:else if !$user$}
  <Login />
{:else}
  <Router {routes} />
{/if}
