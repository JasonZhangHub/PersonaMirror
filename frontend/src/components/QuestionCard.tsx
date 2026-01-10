import type { BFI2Question } from "../types";

type QuestionCardProps = {
  question: BFI2Question;
  value?: number;
  onChange: (value: number) => void;
  scale: Record<string, string>;
};

const scaleNumbers = [1, 2, 3, 4, 5];

export default function QuestionCard({ question, value, onChange, scale }: QuestionCardProps) {
  return (
    <div className="question-card">
      <div className="question-card__text">
        <span className="question-card__id">#{question.id}</span>
        <p>{question.text}</p>
      </div>
      <div className="question-card__scale">
        {scaleNumbers.map((option) => {
          const label = scale[String(option)];
          return (
            <label key={option} className="scale-option">
              <input
                type="radio"
                name={`question-${question.id}`}
                value={option}
                checked={value === option}
                onChange={() => onChange(option)}
              />
              <span>{option}</span>
              <small>{label}</small>
            </label>
          );
        })}
      </div>
    </div>
  );
}
