'use client';

import { useEffect, useState } from 'react';

interface CareerSurveyResult {
  id: number;
  slack_user_id: string;
  result: string;
  created_at: string;
}

type CareerSurveyResults = CareerSurveyResult[];

export const useGetAllSavedCareerSurveyResults = (slackUserId: string) => {
  const [allSavedCareerSurveyResults, setALlSavedCareerSurveyResult] =
    useState<CareerSurveyResults>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);

  useEffect(() => {
    const fetchALlSavedCareerSurveyResults = async () => {
      try {
        const apiUrl = process.env.NEXT_PUBLIC_API_URL;
        const response = await fetch(
          `${apiUrl}/client/print_all_career_survey_results/${slackUserId}/`,
        );

        if (!response.ok) {
          throw new Error(
            `Failed to fetch all saved career survey results.: ${response.status} ${response.statusText}`,
          );
        }
        const allSavedCareerSurveyResults = await response.json();

        if (allSavedCareerSurveyResults.error) {
          throw new Error(allSavedCareerSurveyResults.error);
        }
        setALlSavedCareerSurveyResult(allSavedCareerSurveyResults);
      } catch (err) {
        setError(err instanceof Error ? err : new Error('An unknown error occurred'));
      } finally {
        setLoading(false);
      }
    };

    fetchALlSavedCareerSurveyResults();
  }, []);

  return { allSavedCareerSurveyResults, loading, error };
};
