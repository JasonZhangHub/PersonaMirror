type Step = {
  label: string;
  description: string;
};

type ProgressStepsProps = {
  current: number;
  steps: Step[];
};

export default function ProgressSteps({ current, steps }: ProgressStepsProps) {
  return (
    <div className="steps">
      {steps.map((step, index) => {
        const status = index < current ? "complete" : index === current ? "active" : "upcoming";
        return (
          <div key={step.label} className={`step step--${status}`}>
            <span className="step__index">{index + 1}</span>
            <div>
              <p className="step__label">{step.label}</p>
              <p className="step__description">{step.description}</p>
            </div>
          </div>
        );
      })}
    </div>
  );
}
