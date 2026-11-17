
const SOURCES = [
  { name: 'ANAPEC', body: 'Morocco’s public employment agency.' },
  { name: 'Jobzyn', body: 'A Moroccan job board for local and remote roles.' },
  { name: 'LinkedIn', body: 'Public job postings located in Morocco.' },
];

const Sources = () => (
  <section id="sources" className="border-t border-rule bg-paper">
    <div className="mx-auto max-w-6xl px-4 py-20 sm:px-8 lg:py-24">
      <div className="grid gap-10 lg:grid-cols-[1fr_1.4fr] lg:gap-16">
        <div>
          <h2 className="text-[2rem] font-bold sm:text-[2.5rem]">Where the offers come from</h2>
          <p className="mt-4 text-lg text-graphite">
            Offers are collected from three boards once a day, cleaned up, and kept with a link back to the original
            posting.
          </p>
        </div>
        <dl className="grid gap-8 sm:grid-cols-3">
          {SOURCES.map((source) => (
            <div key={source.name} className="border-t-2 border-ink pt-4">
              <dt className="font-display text-2xl font-bold" style={{ fontVariationSettings: '"wdth" 90' }}>{source.name}</dt>
              <dd className="mt-2 text-graphite">{source.body}</dd>
            </div>
          ))}
        </dl>
      </div>
    </div>
  </section>
);

export default Sources;
