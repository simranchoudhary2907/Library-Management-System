async function loadBooks(){
  const out = document.getElementById('books');
  out.innerHTML = 'Loading...';
  try{
    const res = await fetch('/api/books');
    if(!res.ok) throw new Error('Fetch failed: '+res.status);
    const data = await res.json();
    out.innerHTML = '';
    data.forEach(b => {
      const el = document.createElement('div');
      el.className = 'book';
      el.textContent = `${b.id || ''} ${b.title} — ${b.author || ''}`;
      out.appendChild(el);
    });
  }catch(e){
    out.innerText = 'Error: '+e.message;
  }
}

document.getElementById('load').addEventListener('click', loadBooks);
