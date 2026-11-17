
const Line = ({ w = '100%', hit = false }) => (
  <span className={`block h-1.5 rounded-full ${hit ? 'bg-marker' : 'bg-rule'}`} style={{ width: w }} />
);

/* A small drawing of one document in the pack. */
const Sheet = ({ title, className = '', children }) => (
  <div className={`sheet absolute w-[36%] p-3 shadow-[0_14px_30px_-20px_rgba(20,23,43,0.5)] sm:p-4 ${className}`} aria-hidden="true">
    <p className="mb-3 text-sm font-semibold">{title}</p>
    <div className="space-y-2">{children}</div>
  </div>
);

const DOCS = [
  { name: 'A tailored CV', body: 'Your experience, reordered and reworded around what the offer asks for, in the template you picked.' },
  { name: 'A cover letter', body: 'Addressed to the company, built from the offer’s requirements and your matching experience.' },
  { name: 'An email', body: 'A short message to send with both attachments.' },
];

const ApplicationPack = () => (
  <section id="application" className="border-t border-rule">
    <div className="mx-auto grid max-w-6xl items-center gap-14 px-4 py-20 sm:px-8 lg:grid-cols-2 lg:py-24">
      <div>
        <h2 className="text-[2rem] font-bold sm:text-[2.5rem]">One offer, three documents ready to send</h2>
        <p className="mt-4 max-w-xl text-lg text-graphite">
          Writing a new CV and letter for every offer is the slow part of applying. JobMatcher drafts them from what
          it already knows about you and the offer. You read, adjust and send.
        </p>
        <dl className="mt-8 space-y-5">
          {DOCS.map((doc) => (
            <div key={doc.name}>
              <dt className="font-semibold">{doc.name}</dt>
              <dd className="text-graphite">{doc.body}</dd>
            </div>
          ))}
        </dl>
      </div>

      {/* Three documents laid side by side on the desk. */}
      <div className="relative mx-auto h-64 w-full max-w-lg sm:h-72">
        <Sheet title="CV" className="left-0 top-6 -rotate-3">
          <Line w="60%" /><Line w="90%" hit /><Line /><Line w="75%" hit /><Line w="88%" /><Line w="50%" /><Line w="82%" hit />
        </Sheet>
        <Sheet title="Cover letter" className="left-1/2 top-0 -translate-x-1/2 rotate-1">
          <Line w="55%" /><Line /><Line w="92%" /><Line /><Line w="80%" /><Line w="60%" />
        </Sheet>
        <Sheet title="Email" className="right-0 top-10 rotate-3">
          <Line w="70%" /><Line /><Line w="85%" /><Line w="40%" />
        </Sheet>
      </div>
    </div>
  </section>
);

export default ApplicationPack;
