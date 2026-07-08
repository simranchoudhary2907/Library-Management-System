import React from 'react'

export default function Landing(){
  return (
    <div className="min-h-screen bg-gradient-to-b from-slate-900 via-slate-900 to-slate-800 text-slate-100">
      <header className="container mx-auto p-6 flex items-center justify-between">
        <div className="text-2xl font-bold">LibraFlow</div>
        <nav className="space-x-4">
          <button className="px-4 py-2 rounded-md bg-transparent border border-slate-700">Login</button>
          <button className="px-4 py-2 rounded-md bg-gradient-to-r from-violet-600 to-indigo-500 font-semibold">Get Started</button>
        </nav>
      </header>

      <main className="container mx-auto p-6 grid grid-cols-1 md:grid-cols-2 gap-8 items-center">
        <section className="py-12">
          <h1 className="text-4xl md:text-5xl font-extrabold leading-tight">Manage Your Library. <span className="text-transparent bg-clip-text bg-gradient-to-r from-violet-400 to-indigo-400">Empower Knowledge.</span></h1>
          <p className="mt-6 text-slate-300 max-w-xl">LibraFlow is an all-in-one library management system designed to simplify operations, enhance user experience, and build a smarter library for the future.</p>
          <div className="mt-6 flex gap-4">
            <button className="px-6 py-3 rounded-md bg-gradient-to-r from-violet-600 to-indigo-500 font-semibold">Get Started Free</button>
            <button className="px-6 py-3 rounded-md border border-slate-700">Explore Features</button>
          </div>

          <div className="mt-10 grid grid-cols-2 gap-4">
            <div className="bg-slate-800/60 rounded p-4">
              <div className="text-2xl font-bold">20,000+</div>
              <div className="text-slate-400 text-sm">Total Books</div>
            </div>
            <div className="bg-slate-800/60 rounded p-4">
              <div className="text-2xl font-bold">5,000+</div>
              <div className="text-slate-400 text-sm">Happy Members</div>
            </div>
            <div className="bg-slate-800/60 rounded p-4">
              <div className="text-2xl font-bold">12,000+</div>
              <div className="text-slate-400 text-sm">Books Issued</div>
            </div>
            <div className="bg-slate-800/60 rounded p-4">
              <div className="text-2xl font-bold">99.9%</div>
              <div className="text-slate-400 text-sm">System Uptime</div>
            </div>
          </div>
        </section>

        <section className="flex items-center justify-center">
          <div className="w-full max-w-md p-8 bg-gradient-to-br from-slate-800/60 to-slate-700/40 rounded-xl shadow-lg">
            <div className="h-64 bg-gradient-to-br from-violet-700 to-indigo-700 rounded-md flex items-center justify-center text-white font-semibold">Illustration / Hero Image</div>
          </div>
        </section>
      </main>

      <section className="container mx-auto p-6">
        <h3 className="text-xl mb-4">Why Choose LibraFlow?</h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="bg-slate-800/50 p-6 rounded"> 
            <h4 className="font-semibold">Book Management</h4>
            <p className="text-slate-400 mt-2">Add, update, categorize and manage your book collection easily.</p>
          </div>
          <div className="bg-slate-800/50 p-6 rounded"> 
            <h4 className="font-semibold">Member Management</h4>
            <p className="text-slate-400 mt-2">Register members, track profiles, and member activity.</p>
          </div>
          <div className="bg-slate-800/50 p-6 rounded"> 
            <h4 className="font-semibold">Reports & Analytics</h4>
            <p className="text-slate-400 mt-2">Get insightful reports and analytics to make better decisions.</p>
          </div>
        </div>
      </section>

      <footer className="container mx-auto p-6 text-slate-400">
        <div className="flex flex-col md:flex-row justify-between items-center">
          <div>© 2026 LibraFlow. All rights reserved.</div>
          <div className="space-x-4 mt-4 md:mt-0">
            <a className="hover:underline">Privacy</a>
            <a className="hover:underline">Terms</a>
          </div>
        </div>
      </footer>
    </div>
  )
}
