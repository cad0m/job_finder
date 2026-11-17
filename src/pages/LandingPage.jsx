import { Link } from 'react-router-dom';
import Navbar from '../components/Navbar';
import Hero from '../components/Hero';
import HowItWorks from '../components/HowItWorks';
import ApplicationPack from '../components/ApplicationPack';
import Sources from '../components/Sources';
import Footer from '../components/Footer';

const LandingPage = () => (
  <div className="min-h-screen">
    <Navbar />
    <main>
      <Hero />
      <HowItWorks />
      <ApplicationPack />
      <Sources />

      <section className="bg-ink text-white">
        <div className="mx-auto flex max-w-6xl flex-col items-start gap-6 px-4 py-16 sm:px-8 md:flex-row md:items-center md:justify-between">
          <h2 className="max-w-xl text-[2rem] font-bold sm:text-[2.5rem]">Start with the CV you already have.</h2>
          <Link to="/upload" className="btn btn-lg bg-white text-ink hover:bg-desk">Upload your CV</Link>
        </div>
      </section>
    </main>
    <Footer />
  </div>
);

export default LandingPage;
