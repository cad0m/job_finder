
const STEPS = [
  {
    title: 'Upload your CV',
    body: 'A PDF works best. A clear photo or scan (JPEG, PNG, WEBP) works too.',
  },
  {
    title: 'Check what was read',
    body: 'JobMatcher pulls out your experience, skills, education and languages. Correct anything it got wrong before you save.',
  },
  {
    title: 'Read your ranked offers',
    body: 'Every offer gets a match score from comparing its description with your CV. You can also describe the job you want in your own words.',
  },
  {
    title: 'Generate the application',
    body: 'Pick an offer and a CV template. You get a CV, a cover letter and an email written for that offer, as PDFs.',
  },
];

const HowItWorks = () => (
  <section id="how-it-works" className="border-t border-rule bg-paper">
    <div className="mx-auto max-w-6xl px-4 py-20 sm:px-8 lg:py-24">
      <h2 className="max-w-2xl text-[2rem] font-bold sm:text-[2.5rem]">From one CV to a finished application, in four steps</h2>

      <ol className="mt-12 grid gap-x-12 gap-y-10 sm:grid-cols-2 lg:grid-cols-4">
        {STEPS.map((step, i) => (
          <li key={step.title} className="border-t-2 border-ink pt-4">
            <span className="font-display text-[2.5rem] font-bold leading-none text-ink" style={{ fontVariationSettings: '"wdth" 85' }} aria-hidden="true">
              {i + 1}
            </span>
            <h3 className="mt-3 font-sans text-lg font-semibold tracking-normal">{step.title}</h3>
            <p className="mt-2 text-graphite">{step.body}</p>
          </li>
        ))}
      </ol>
    </div>
  </section>
);

export default HowItWorks;
