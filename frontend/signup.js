const form = document.querySelector("#signup-form");

const checkPassword = () => {
  const formData = new FormData(form);
  const password1 = formData.get("password");
  const password2 = formData.get("password2");

  if (password1 === password2) {
    return true;
  } else return false;
};
const handleSubmit = async (event) => {
  event.preventDefault();
  const formData = new FormData(form);
  const sha256Password = sha256(formData.get("password"));
  formData.set("password", sha256Password);
  console.log(formData.get("password"));

  const div = document.querySelector("#info");

  if (checkPassword()) {
    const res = await fetch("/signup", {
      method: "POST",
      body: formData,
    });
    const data = await res.json();
    if (data == "200") {
      alert("회원 가입 성공");
      window.location.pathname = "/login.html";
    }
    //기존 아이디가 존재하면 회원가입할 수 없도록 로직 짜기
  } else {
    div.innerText = "비밀번호가 같지 않습니다";
    div.style.color = "red";
  }
};

form.addEventListener("submit", handleSubmit);
